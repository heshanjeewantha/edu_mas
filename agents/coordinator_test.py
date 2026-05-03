# agents/coordinator.py
"""
Coordinator Agent — Student A

Validates the student's topic, fetches a factual knowledge base
from Wikipedia, and prepares context for the Quiz Generator.
"""
from crewai import Agent


def create_coordinator(llm) -> Agent:
    """
    Create and return the Coordinator agent.

    The Coordinator is the entry point of the pipeline. It:
    - Validates the topic is suitable for an educational quiz
    - Uses the Wikipedia tool to fetch an accurate factual summary
    - Passes a clean, grounded context to the next agent

    Args:
        llm: The local Ollama LLM instance to power this agent.

    Returns:
        Agent: A configured CrewAI Agent instance.
    """
    return Agent(
        role="Education Coordinator",
        goal=(
            "Validate the student's requested topic and difficulty level. "
            "Fetch an accurate, factual topic summary from Wikipedia using the "
            "wikipedia_topic_fetcher tool. Return ONLY the raw summary text — "
            "do not add commentary, opinions, or invented facts."
        ),
        backstory=(
            "You are a senior academic coordinator at an elite online learning platform. "
            "You have 15 years of experience validating educational content. "
            "Your golden rule: NEVER invent facts. If Wikipedia doesn't have it, say so. "
            "You are meticulous, structured, and brief. You prepare the knowledge "
            "base that all downstream agents depend on — accuracy is everything."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_rpm=10,
    )
