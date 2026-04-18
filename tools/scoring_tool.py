# tools/scoring_tool.py
"""
Answer Scoring Tool — Student C's custom tool.

Reads a saved quiz JSON file and scores the student's answers
against the correct answer key. Used by the Grader agent.
"""
import json
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from logger import log_tool_call, log_tool_result, log_error


class ScoringSchema(BaseModel):
    """Input schema for the AnswerScoringTool."""
    quiz_path: str = Field(
        ...,
        description="Relative path to the saved quiz JSON file (e.g. 'output/quiz.json')"
    )
    student_answers: str = Field(
        ...,
        description=(
            "Comma-separated student answer choices corresponding to each question. "
            "Each value must be A, B, C, or D. Example: 'A,B,C,A,D'"
        )
    )


class AnswerScoringTool(BaseTool):
    """
    Reads a quiz JSON file and scores the student's submitted answers
    against the correct answer key stored in the file.

    Used by the Grader agent to produce a structured score breakdown
    for each question, plus an overall percentage score.

    Args:
        quiz_path (str): Relative path to the quiz JSON file (e.g. 'output/quiz.json').
        student_answers (str): Comma-separated answer letters, one per question
            (e.g. 'A,B,C,A,D'). Must match the number of questions in the file.

    Returns:
        str: A JSON string containing:
            - 'results': list of per-question dicts with question text,
              student answer, correct answer, and is_correct flag.
            - 'score_percentage': overall percentage score (float, 0-100).
            Or an error message prefixed with 'ERROR:'.
    """
    name: str = "score_student_answers"
    description: str = (
        "Reads the quiz JSON file and scores the student's answers against the answer key. "
        "Input: quiz_path (path to quiz file), student_answers (comma-separated A/B/C/D). "
        "Returns a JSON string with per-question results and total score percentage."
    )
    args_schema: type[BaseModel] = ScoringSchema

    def _run(self, quiz_path: str, student_answers: str) -> str:
        log_tool_call("score_student_answers", {"quiz_path": quiz_path, "student_answers": student_answers})
        try:
            with open(quiz_path, "r", encoding="utf-8") as f:
                questions = json.load(f)

            if not isinstance(questions, list) or len(questions) == 0:
                return "ERROR: Quiz file is empty or malformed."

            raw_answers = [a.strip().upper() for a in student_answers.split(",")]
            valid_choices = {"A", "B", "C", "D"}

            results = []
            correct_count = 0

            for i, q in enumerate(questions):
                student_ans = raw_answers[i] if i < len(raw_answers) else "N/A"
                correct_ans = str(q.get("answer", "")).strip().upper()

                if student_ans not in valid_choices:
                    student_ans = "INVALID"

                is_correct = student_ans == correct_ans
                if is_correct:
                    correct_count += 1

                results.append({
                    "question_no": i + 1,
                    "question": q.get("question", f"Question {i+1}"),
                    "student_answer": student_ans,
                    "correct_answer": correct_ans,
                    "is_correct": is_correct,
                })

            score_pct = round((correct_count / len(questions)) * 100, 1)
            output = {
                "results": results,
                "correct_count": correct_count,
                "total_questions": len(questions),
                "score_percentage": score_pct,
            }
            result_str = json.dumps(output, indent=2)
            log_tool_result("score_student_answers", f"Score={score_pct}% ({correct_count}/{len(questions)})")
            return result_str

        except FileNotFoundError:
            error_msg = f"ERROR: Quiz file not found at '{quiz_path}'. Ensure the Quiz Generator ran first."
            log_error("AnswerScoringTool", error_msg)
            return error_msg
        except json.JSONDecodeError as e:
            error_msg = f"ERROR: Quiz file contains invalid JSON — {str(e)}"
            log_error("AnswerScoringTool", error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"ERROR scoring answers: {str(e)}"
            log_error("AnswerScoringTool", error_msg)
            return error_msg
