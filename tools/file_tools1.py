# tools/file_tools.py
"""
Quiz File Writer Tool.

Saves generated quiz questions to a local JSON file in output/.
Used by the Quiz Generator agent.
"""
import json
import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from logger import log_tool_call, log_tool_result, log_error


class QuizSaveSchema(BaseModel):
    """Input schema for the SaveQuizTool."""
    quiz_json: str = Field(
        ...,
        description=(
            "Quiz questions as a JSON string. Must be a list of objects, each with: "
            "'question' (str), 'options' (dict with keys A-D), 'answer' (str, one of A/B/C/D)."
        )
    )
    filename: str = Field(
        default="quiz.json",
        description="Output filename inside the output/ directory (default: quiz.json)"
    )


class SaveQuizTool(BaseTool):
    """
    Saves generated quiz questions to a local JSON file in the output/ directory.

    Validates that the input is a properly structured JSON list before saving.
    Used by the Quiz Generator agent after question generation is complete.

    Args:
        quiz_json (str): A JSON string containing a list of quiz question objects.
            Each object must have keys: 'question', 'options' (A-D), 'answer'.
        filename (str): The output filename. Defaults to 'quiz.json'.

    Returns:
        str: A success message with the saved file path, or an error message
             prefixed with 'ERROR:' describing what went wrong.
    """
    name: str = "save_quiz_to_file"
    description: str = (
        "Saves the generated quiz questions to a JSON file in the output/ directory. "
        "Input: quiz_json (JSON string list of question objects), filename (optional). "
        "Always call this after generating questions."
    )
    args_schema: type[BaseModel] = QuizSaveSchema

    def _run(self, quiz_json: str, filename: str = "quiz.json") -> str:
        log_tool_call("save_quiz_to_file", {"filename": filename, "quiz_length": len(quiz_json)})
        try:
            os.makedirs("output", exist_ok=True)
            path = os.path.join("output", filename)

            # Validate JSON
            data = json.loads(quiz_json)
            if not isinstance(data, list):
                return "ERROR: quiz_json must be a JSON array (list), not an object."
            if len(data) == 0:
                return "ERROR: quiz_json array is empty — no questions to save."

            # Validate each question has required keys
            for i, q in enumerate(data):
                missing = [k for k in ("question", "options", "answer") if k not in q]
                if missing:
                    return f"ERROR: Question {i+1} is missing keys: {missing}"

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            result = f"SUCCESS: {len(data)} questions saved to {path}"
            log_tool_result("save_quiz_to_file", result)
            return result

        except json.JSONDecodeError as e:
            error_msg = f"ERROR: Invalid JSON provided — {str(e)}"
            log_error("SaveQuizTool", error_msg)
            return error_msg
        except PermissionError:
            error_msg = "ERROR: Permission denied writing to output/ directory."
            log_error("SaveQuizTool", error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"ERROR saving quiz: {str(e)}"
            log_error("SaveQuizTool", error_msg)
            return error_msg
