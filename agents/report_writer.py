# agents/report_writer.py
"""
Report Writer Agent — Student D

Compiles all pipeline outputs into a clean, structured JSON report
saved to the output/ directory with a timestamp.
"""
from crewai import Agent


def create_report_writer(llm) -> Agent:
    """
    Create and return the Report Writer agent.

    The Report Writer:
    - Receives the topic, student name, and score JSON from the Grader
    - Uses the write_final_report tool to compile and save the report
    - Returns the file path of the saved report

    Args:
        llm: The local Ollama LLM instance to power this agent.

    Returns:
        Agent: A configured CrewAI Agent instance.
    """
    return Agent(
        role="Academic Report Writer",
        goal=(
            "Use the write_final_report tool to compile the quiz topic, student name, "
            "and grading results into a structured report saved to disk. "
            "Return the file path of the saved report. Do NOT invent any data."
        ),
        backstory=(
            "You are a precise technical writer who produces clean, structured academic reports "
            "for an online learning management system. "
            "You never add information that wasn't explicitly provided. "
            "You never modify scores or results. "
            "Your reports are always valid, well-structured JSON saved properly to disk. "
            "You are the final step in the pipeline — accuracy and completeness are paramount."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_rpm=10,
    )
