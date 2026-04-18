# main.py
"""
EduMAS — Educational Multi-Agent System
SE4010 CTSE Assignment 2

Entry point for the full pipeline:
  Coordinator → Quiz Generator → Grader → Report Writer

Run: python main.py
Requires: ollama serve (in a separate terminal)
"""
import os
import sys
import json
import re

from crewai import Crew, Task, LLM


from agents.coordinator import create_coordinator
from agents.quiz_generator import create_quiz_generator

from tools.api_tool import WikipediaTool
from tools.file_tools import SaveQuizTool
from tools.scoring_tool import AnswerScoringTool
from tools.report_tool import WriteReportTool

from state import EduMASState
from logger import (
    log_pipeline_start,
    log_pipeline_end,
    log_state_transition,
    crewai_step_callback,
    logger,
)


def _repair_common_json_issues(payload: str) -> str:
    """Repair common lightweight JSON issues produced by local models."""
    repaired = payload
    repaired = repaired.replace("\u201c", '"').replace("\u201d", '"')
    repaired = repaired.replace("\u2018", "'").replace("\u2019", "'")

    # Fix merged option token such as "D: option text" -> "D":"option text"
    repaired = re.sub(r'"([A-D])\s*:\s*([^"\n]+)"', r'"\1":"\2"', repaired)

    # Fix malformed option keys such as "D: ..." -> "D": "..."
    repaired = re.sub(r'([\{,]\s*)"([A-D])\s*:', r'\1"\2":', repaired)
    repaired = re.sub(r'([\{,]\s*)([A-D])\s*:', r'\1"\2":', repaired)
    return repaired


def _extract_json_array(text: str) -> str:
    """Extract the first JSON array from model output."""
    # Remove fenced code blocks if present.
    cleaned = text.strip().replace("```json", "").replace("```", "")
    match = re.search(r"\[[\s\S]*\]", cleaned)
    if not match:
        raise ValueError("Could not find a JSON array in model output.")

    candidate = match.group(0)
    try:
        json.loads(candidate)  # Validate parseability.
        return candidate
    except json.JSONDecodeError:
        repaired = _repair_common_json_issues(candidate)
        json.loads(repaired)  # Raise if still invalid.
        return repaired

os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ── Pipeline configuration ──────────────────────────────────────────────────
TOPIC      = "Photosynthesis"
DIFFICULTY = "medium"         # easy | medium | hard
STUDENT    = "Alice Fernando"
ANSWERS    = "A,B,C,A,D"     # simulated student answers (one per question)

# ── Global shared state (passed between agents) ─────────────────────────────
state = EduMASState(
    topic=TOPIC,
    difficulty=DIFFICULTY,
    student_name=STUDENT,
    student_answers=ANSWERS.split(","),
)

# ── LLM config for CrewAI ──────────────────────────────────────────────────
llm = LLM(
    model="ollama/phi3:mini",
    base_url="http://localhost:11434",
    temperature=0.1,   # low temperature for factual accuracy
)

# ── Tools ──────────────────────────────────────────────────────────────────
wiki_tool   = WikipediaTool()
save_quiz   = SaveQuizTool()
score_tool  = AnswerScoringTool()
report_tool = WriteReportTool()

# ── Agents ──────────────────────────────────────────────────────────────────
coordinator    = create_coordinator(llm)
quiz_generator = create_quiz_generator(llm)

# ── Tasks (sequential pipeline with context chaining = state passing) ────────

task1 = Task(
    description=(
        f"TOPIC: '{state.topic}' | DIFFICULTY: '{state.difficulty}'\n\n"
        f"You are given a trusted Wikipedia summary below. Rewrite it as a clear "
        f"study note for a {state.difficulty}-level student in 4-7 sentences. "
        f"Return plain text only.\n\n"
        f"WIKIPEDIA SUMMARY:\n{wiki_tool._run(state.topic)}"
    ),
    expected_output=(
        "A clear factual study note in plain text, 4-7 sentences."
    ),
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
        f"- options object must use exact keys \"A\", \"B\", \"C\", \"D\"\n"
        f"- each key must be followed by a colon, e.g. \"D\": \"...\"\n"
        f"- Return ONLY the JSON array. Do not include markdown, explanations, or extra text."
    ),
    expected_output=(
        "A valid JSON array containing exactly 5 MCQ objects."
    ),
    agent=quiz_generator,
    context=[task1],
)

# ── Crew with step_callback for full observability ───────────────────────────
crew = Crew(
    agents=[coordinator, quiz_generator],
    tasks=[task1, task2],
    verbose=True,
    step_callback=crewai_step_callback,   # 🔍 logs every agent step automatically
)

# ── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log_pipeline_start(state.topic, state.student_name, state.difficulty)

    # Log state being passed into pipeline
    state.log("main", f"Pipeline initialised | topic={state.topic} | difficulty={state.difficulty}")
    log_state_transition("main", "Coordinator", ["topic", "difficulty", "student_name"])

    try:
        result = crew.kickoff()
        result_str = str(result)
        quiz_json = _extract_json_array(result_str)

        save_result = save_quiz._run(quiz_json=quiz_json, filename="quiz.json")
        if save_result.startswith("ERROR"):
            raise RuntimeError(save_result)

        score_json = score_tool._run(quiz_path="output/quiz.json", student_answers=ANSWERS)
        if score_json.startswith("ERROR"):
            raise RuntimeError(score_json)

        report_result = report_tool._run(
            topic=state.topic,
            score_json=score_json,
            student_name=state.student_name,
            difficulty=state.difficulty,
        )
        if report_result.startswith("ERROR"):
            raise RuntimeError(report_result)

        score_obj = json.loads(score_json)
        final_score = float(score_obj.get("score_percentage", 0.0))

        # Update state with pipeline result
        state.final_report_path = report_result
        state.log("ReportWriter", f"Pipeline complete | result={report_result[:100]}")

        log_pipeline_end(report_result, score=final_score)

        print("\n" + "="*60)
        print("✅  EduMAS pipeline complete!")
        print("="*60)
        print(f"📄  Quiz saved to    : output/quiz.json")
        print(f"📊  Report saved to  : output/report_*.json")
        print(f"🔍  Full trace log   : logs/agent_trace.log")
        print("="*60)

    except Exception as e:
        state.error = str(e)
        state.log("main", f"PIPELINE FAILED: {e}")
        logger.error(f"[FATAL] Pipeline failed: {e}")
        print(f"\n❌ Pipeline failed: {e}")
        print("Check logs/agent_trace.log for details.")
        sys.exit(1)
