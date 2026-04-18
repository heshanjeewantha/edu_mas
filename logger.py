# logger.py
"""
LLMOps / AgentOps observability module for EduMAS.

Records all agent inputs, tool calls, and outputs to both the
terminal and a persistent log file at logs/agent_trace.log.
"""
import logging
import os
import json
from datetime import datetime
from typing import Any

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/agent_trace.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("EduMAS")


def log_agent_start(agent_name: str, input_data: str) -> None:
    """Log when an agent begins processing."""
    logger.info(f"[START] Agent={agent_name} | Input={str(input_data)[:300]}")


def log_agent_end(agent_name: str, output_data: str) -> None:
    """Log when an agent finishes processing."""
    logger.info(f"[END]   Agent={agent_name} | Output={str(output_data)[:300]}")


def log_tool_call(tool_name: str, args: dict[str, Any]) -> None:
    """Log a tool invocation with its arguments."""
    logger.info(f"[TOOL]  Tool={tool_name} | Args={json.dumps(args, default=str)[:300]}")


def log_tool_result(tool_name: str, result: str) -> None:
    """Log the result returned by a tool."""
    logger.info(f"[RESULT] Tool={tool_name} | Result={str(result)[:300]}")


def log_state_transition(from_agent: str, to_agent: str, state_keys: list[str]) -> None:
    """Log state being handed from one agent to the next."""
    logger.info(
        f"[STATE] {from_agent} → {to_agent} | Keys transferred={state_keys}"
    )


def log_error(agent_name: str, error: str) -> None:
    """Log an error encountered by an agent."""
    logger.error(f"[ERROR] Agent={agent_name} | Error={error}")


def log_pipeline_start(topic: str, student: str, difficulty: str) -> None:
    """Log the start of a full pipeline run."""
    logger.info("=" * 70)
    logger.info(
        f"[PIPELINE START] Topic={topic} | Student={student} | Difficulty={difficulty} | Time={datetime.now().isoformat()}"
    )
    logger.info("=" * 70)


def log_pipeline_end(report_path: str, score: float) -> None:
    """Log the successful completion of a pipeline run."""
    logger.info("=" * 70)
    logger.info(
        f"[PIPELINE END] Report={report_path} | Score={score}% | Time={datetime.now().isoformat()}"
    )
    logger.info("=" * 70)


def crewai_step_callback(step_output: Any) -> None:
    """
    Callback hooked into CrewAI's step_callback to auto-log every
    agent action, tool call, and intermediate output.
    """
    try:
        logger.info(f"[STEP] {str(step_output)[:500]}")
    except Exception:
        pass
