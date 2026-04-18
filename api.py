# api.py
"""
EduMAS — Flask REST API
Exposes the pipeline to the frontend via HTTP endpoints.

Run: python api.py
Requires: ollama serve (separate terminal)
"""
import os
import sys
import json
import re
import glob
from flask import Flask, request, jsonify
from flask_cors import CORS

from crewai import Crew, Task, LLM
from agents.coordinator import create_coordinator
from agents.quiz_generator import create_quiz_generator
from tools.api_tool import WikipediaTool
from tools.file_tools import SaveQuizTool
from tools.scoring_tool import AnswerScoringTool
from tools.report_tool import WriteReportTool
from state import EduMASState
from logger import log_pipeline_start, log_pipeline_end, log_state_transition, crewai_step_callback, logger

app = Flask(__name__)
CORS(app)  # Allow frontend (Vite dev server) to call this API

os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)


def _repair_common_json_issues(payload: str) -> str:
    repaired = payload
    repaired = repaired.replace("\u201c", '"').replace("\u201d", '"')
    repaired = repaired.replace("\u2018", "'").replace("\u2019", "'")
    repaired = re.sub(r'"([A-D])\s*:\s*([^"\n]+)"', r'"\1":"\2"', repaired)
    repaired = re.sub(r'([\{,]\s*)"([A-D])\s*:', r'\1"\2":', repaired)
    repaired = re.sub(r'([\{,]\s*)([A-D])\s*:', r'\1"\2":', repaired)
    return repaired


def _extract_json_array(text: str) -> str:
    cleaned = text.strip().replace("```json", "").replace("```", "")
    match = re.search(r"\[[\s\S]*\]", cleaned)
    if not match:
        raise ValueError("Could not find a JSON array in model output.")
    candidate = match.group(0)
    try:
        json.loads(candidate)
        return candidate
    except json.JSONDecodeError:
        repaired = _repair_common_json_issues(candidate)
        json.loads(repaired)
        return repaired


# ── Endpoint: POST /api/run ───────────────────────────────────────────────────
@app.route("/api/run", methods=["POST"])
def run_pipeline():
    """
    Run the full EduMAS pipeline.
    Body JSON: { topic, difficulty, student_name, answers }
    answers: comma-separated string like "A,B,C,A,D"
    Returns: { quiz, score, report, report_file }
    """
    try:
        data = request.get_json(force=True)
        topic = data.get("topic", "Photosynthesis").strip()
        difficulty = data.get("difficulty", "medium").strip()
        student_name = data.get("student_name", "Student").strip()
        answers = data.get("answers", "A,A,A,A,A").strip()

        state = EduMASState(
            topic=topic,
            difficulty=difficulty,
            student_name=student_name,
            student_answers=answers.split(","),
        )

        llm = LLM(
            model="ollama/phi3:mini",
            base_url="http://localhost:11434",
            temperature=0.1,
        )

        wiki_tool   = WikipediaTool()
        save_quiz   = SaveQuizTool()
        score_tool  = AnswerScoringTool()
        report_tool = WriteReportTool()

        coordinator    = create_coordinator(llm)
        quiz_generator = create_quiz_generator(llm)

        # Fetch Wikipedia summary and store it to return to the frontend
        wiki_summary = wiki_tool._run(state.topic)

        task1 = Task(
            description=(
                f"TOPIC: '{state.topic}' | DIFFICULTY: '{state.difficulty}'\n\n"
                f"You are given a trusted Wikipedia summary below. Rewrite it as a clear "
                f"study note for a {state.difficulty}-level student in 4-7 sentences. "
                f"Return plain text only.\n\n"
                f"WIKIPEDIA SUMMARY:\n{wiki_summary}"
            ),
            expected_output="A clear factual study note in plain text, 4-7 sentences.",
            agent=coordinator,
        )

        task2 = Task(
            description=(
                f"Using the topic summary from the previous task, generate exactly 5 "
                f"multiple-choice questions at '{state.difficulty}' difficulty level. "
                f"Each question must have options A, B, C, D and one correct answer.\n\n"
                f"Output format - a valid JSON array:\n"
                f'[{{"question": "...", "options": {{"A":"...", "B":"...", "C":"...", "D":"..."}}, "answer": "A"}}]\n\n'
                f"Rules:\n"
                f'- options object must use exact keys "A", "B", "C", "D"\n'
                f'- each key must be followed by a colon, e.g. "D": "..."\n'
                f"- Return ONLY the JSON array. Do not include markdown, explanations, or extra text."
            ),
            expected_output="A valid JSON array containing exactly 5 MCQ objects.",
            agent=quiz_generator,
            context=[task1],
        )

        crew = Crew(
            agents=[coordinator, quiz_generator],
            tasks=[task1, task2],
            verbose=True,
            step_callback=crewai_step_callback,
        )

        log_pipeline_start(state.topic, state.student_name, state.difficulty)
        log_state_transition("api", "Coordinator", ["topic", "difficulty", "student_name"])

        result = crew.kickoff()
        result_str = str(result)
        quiz_json = _extract_json_array(result_str)

        save_result = save_quiz._run(quiz_json=quiz_json, filename="quiz.json")
        if save_result.startswith("ERROR"):
            return jsonify({"error": save_result}), 500

        score_json = score_tool._run(quiz_path="output/quiz.json", student_answers=answers)
        if score_json.startswith("ERROR"):
            return jsonify({"error": score_json}), 500

        report_result = report_tool._run(
            topic=state.topic,
            score_json=score_json,
            student_name=state.student_name,
            difficulty=state.difficulty,
        )
        if report_result.startswith("ERROR"):
            return jsonify({"error": report_result}), 500

        score_obj  = json.loads(score_json)
        quiz_questions = json.loads(quiz_json)

        # Read the saved report file
        report_files = sorted(glob.glob("output/report_*.json"), reverse=True)
        report_data = {}
        report_filename = ""
        if report_files:
            report_filename = os.path.basename(report_files[0])
            with open(report_files[0], "r", encoding="utf-8") as f:
                report_data = json.load(f)

        log_pipeline_end(report_result, score=float(score_obj.get("score_percentage", 0)))

        return jsonify({
            "quiz": quiz_questions,
            "score": score_obj,
            "report": report_data,
            "report_file": report_filename,
            "wiki_summary": wiki_summary,
        })

    except Exception as e:
        logger.error(f"[API ERROR] {e}")
        return jsonify({"error": str(e)}), 500


# ── Endpoint: GET /api/wiki ──────────────────────────────────────────────────
@app.route("/api/wiki", methods=["GET"])
def get_wiki():
    """Fetch Wikipedia summary for a topic quickly (no LLM)."""
    topic = request.args.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "topic query param is required"}), 400
    try:
        wiki_tool = WikipediaTool()
        summary = wiki_tool._run(topic)
        return jsonify({"topic": topic, "summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Endpoint: GET /api/quiz ───────────────────────────────────────────────────
@app.route("/api/quiz", methods=["GET"])
def get_quiz():
    """Return the last saved quiz."""
    quiz_path = "output/quiz.json"
    if not os.path.exists(quiz_path):
        return jsonify({"error": "No quiz generated yet."}), 404
    with open(quiz_path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


# ── Endpoint: GET /api/report ─────────────────────────────────────────────────
@app.route("/api/report", methods=["GET"])
def get_report():
    """Return the most recent report."""
    files = sorted(glob.glob("output/report_*.json"), reverse=True)
    if not files:
        return jsonify({"error": "No report generated yet."}), 404
    with open(files[0], "r", encoding="utf-8") as f:
        return jsonify({"filename": os.path.basename(files[0]), "report": json.load(f)})


# ── Endpoint: GET /api/health ─────────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "EduMAS API"})


if __name__ == "__main__":
    print("=" * 60)
    print("EduMAS API starting on http://localhost:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)
