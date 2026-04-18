# agents/quiz_generator.py
"""
Quiz Generator Agent — Student B

Generates exactly 5 multiple-choice questions from the topic summary
and saves them to a local JSON file.
"""
from crewai import Agent


def create_quiz_generator(llm) -> Agent:
    """
    Create and return the Quiz Generator agent.

    The Quiz Generator:
    - Reads the topic summary passed from the Coordinator
    - Generates exactly 5 MCQ questions at the requested difficulty
    - Formats output as a strict JSON array
    - Saves the quiz to output/quiz.json using the save_quiz_to_file tool

    Args:
        llm: The local Ollama LLM instance to power this agent.

    Returns:
        Agent: A configured CrewAI Agent instance.
    """
    return Agent(
        role="Quiz Generator",
        goal=(
            "Using ONLY the topic summary provided, generate exactly 5 "
            "multiple-choice questions at the specified difficulty level. "
            "Each question must have options A, B, C, D and exactly one correct answer. "
            "Output as a valid JSON array. Then save it using the save_quiz_to_file tool."
        ),
        backstory=(
            "You are an expert educational content creator with a PhD in Instructional Design. "
            "You follow Bloom's Taxonomy strictly: easy = recall, medium = comprehension, "
            "hard = application and analysis. "
            "You NEVER invent facts outside the provided summary. "
            "You NEVER produce malformed JSON — your output must be parseable. "
            "You write clear, unambiguous questions with one definitively correct answer."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_rpm=10,
    )
