# tools/report_tool.py
"""
Final Report Writer Tool — Student D's custom tool.

Compiles all pipeline outputs into a structured JSON report saved
to the output/ directory with a timestamp. Used by the Report Writer agent.
"""
import json
import os
from datetime import datetime
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from logger import log_tool_call, log_tool_result, log_error


class ReportSchema(BaseModel):
    """Input schema for the WriteReportTool."""
    topic: str = Field(
        ...,
        description="The educational topic that was tested (e.g. 'Photosynthesis')"
    )
    score_json: str = Field(
        ...,
        description=(
            "The full scoring results as a JSON string, as returned by the "
            "score_student_answers tool. Must contain 'results' and 'score_percentage'."
        )
    )
    student_name: str = Field(
        default="Student",
        description="The full name of the student being assessed"
    )
    difficulty: str = Field(
        default="medium",
        description="Difficulty level of the quiz: 'easy', 'medium', or 'hard'"
    )


class WriteReportTool(BaseTool):
    """
    Compiles quiz results into a well-structured JSON academic report and
    saves it to the output/ directory with a UTC timestamp in the filename.

    Used by the Report Writer agent as the final step in the pipeline.

    Args:
        topic (str): The educational topic that was assessed.
        score_json (str): JSON string of scoring results from the Grader agent.
            Must contain 'results' (list) and 'score_percentage' (float).
        student_name (str): The student's name. Defaults to 'Student'.
        difficulty (str): Quiz difficulty level. Defaults to 'medium'.

    Returns:
        str: A success message with the saved report file path, or an error
             message prefixed with 'ERROR:' describing what went wrong.
    """
    name: str = "write_final_report"
    description: str = (
        "Compiles quiz results into a structured JSON report and saves it to output/. "
        "Input: topic (str), score_json (JSON string from grader), "
        "student_name (str, optional), difficulty (str, optional). "
        "Always call this last, after grading is complete."
    )
    args_schema: type[BaseModel] = ReportSchema

    def _run(
        self,
        topic: str,
        score_json: str,
        student_name: str = "Student",
        difficulty: str = "medium",
    ) -> str:
        log_tool_call(
            "write_final_report",
            {"topic": topic, "student_name": student_name, "difficulty": difficulty}
        )
        try:
            os.makedirs("output", exist_ok=True)

            scores = json.loads(score_json)
            score_pct = scores.get("score_percentage", 0)
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.json"
            path = os.path.join("output", filename)

            # Determine pass/fail threshold (60%)
            pass_status = "PASS" if score_pct >= 60 else "FAIL"

            # Generate per-question feedback
            feedback = []
            for r in scores.get("results", []):
                entry = {
                    "question_no": r.get("question_no"),
                    "question": r.get("question"),
                    "student_answer": r.get("student_answer"),
                    "correct_answer": r.get("correct_answer"),
                    "result": "Correct" if r.get("is_correct") else "Incorrect",
                }
                feedback.append(entry)

            report = {
                "report_metadata": {
                    "generated_at_utc": timestamp,
                    "pipeline": "EduMAS v1.0",
                    "framework": "CrewAI + Ollama",
                },
                "student": {
                    "name": student_name,
                    "topic": topic,
                    "difficulty": difficulty,
                },
                "results": {
                    "score_percentage": score_pct,
                    "correct_count": scores.get("correct_count", 0),
                    "total_questions": scores.get("total_questions", 5),
                    "pass_status": pass_status,
                    "pass_threshold_percent": 60,
                },
                "question_feedback": feedback,
            }

            with open(path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            result = f"SUCCESS: Report saved to {path} | Score={score_pct}% | Status={pass_status}"
            log_tool_result("write_final_report", result)
            return result

        except json.JSONDecodeError as e:
            error_msg = f"ERROR: score_json is not valid JSON — {str(e)}"
            log_error("WriteReportTool", error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"ERROR writing report: {str(e)}"
            log_error("WriteReportTool", error_msg)
            return error_msg
