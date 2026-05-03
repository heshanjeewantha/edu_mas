# agents/grader.py
"""
Grader Agent — Student C

Evaluates student answers against the answer key and produces
a detailed, per-question score breakdown.
"""
from crewai import Agent


def create_grader(llm) -> Agent:
    """
    Create and return the Grader agent.

    The Grader:
    - Reads the saved quiz file using the score_student_answers tool
    - Compares each student answer to the correct answer
    - Returns a structured JSON score report
    - Provides a one-line explanation for each wrong answer

    Args:
        llm: The local Ollama LLM instance to power this agent.

    Returns:
        Agent: A configured CrewAI Agent instance.
    """
    return Agent(
        role="Automated Grader",
        goal=(
            "Use the score_student_answers tool to evaluate the student's answers "
            "against the quiz answer key. Return the full score JSON exactly as "
            "the tool returns it — do NOT modify, round, or reinterpret the scores."
        ),
        backstory=(
            "You are a strict but fair academic grader with 20 years of exam marking experience. "
            "You evaluate answers objectively against the answer key — no partial credit unless told. "
            "You never give marks for guesses. You never invent explanations. "
            "Your feedback is concise, factual, and constructive. "
            "You always return the raw tool output without modification."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_rpm=10,
    )
