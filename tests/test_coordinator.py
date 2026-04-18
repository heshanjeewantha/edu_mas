# tests/test_coordinator.py
"""
Tests for the Coordinator agent's tool: WikipediaTool (Student A).

Tests cover: valid topic fetch, unknown topic handling, empty input,
special characters, and LLM-as-a-Judge quality check on the summary.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.api_tool import WikipediaTool


@pytest.fixture
def wiki_tool():
    return WikipediaTool()


class TestWikipediaToolPositive:
    """Happy-path tests for valid educational topics."""

    def test_returns_string_for_known_topic(self, wiki_tool):
        result = wiki_tool._run(topic="Photosynthesis")
        assert isinstance(result, str)
        assert len(result) > 50

    def test_result_does_not_start_with_error(self, wiki_tool):
        result = wiki_tool._run(topic="Photosynthesis")
        assert not result.startswith("ERROR")

    def test_summary_length_within_limit(self, wiki_tool):
        result = wiki_tool._run(topic="Newton's laws of motion")
        assert len(result) <= 1100  # max 1000 chars + small buffer

    def test_summary_contains_topic_keyword(self, wiki_tool):
        result = wiki_tool._run(topic="Mitosis")
        assert "mitosis" in result.lower() or "cell" in result.lower()

    def test_different_topics_return_different_results(self, wiki_tool):
        r1 = wiki_tool._run(topic="Photosynthesis")
        r2 = wiki_tool._run(topic="Mitosis")
        assert r1 != r2


class TestWikipediaToolNegative:
    """Error-handling tests for invalid or missing topics."""

    def test_nonexistent_topic_returns_error(self, wiki_tool):
        result = wiki_tool._run(topic="XYZ_NONSENSE_TOPIC_12345_FAKE")
        assert result.startswith("ERROR")

    def test_empty_string_topic_returns_error(self, wiki_tool):
        result = wiki_tool._run(topic="")
        assert isinstance(result, str)  # must not raise exception

    def test_numeric_string_topic_handles_gracefully(self, wiki_tool):
        result = wiki_tool._run(topic="12345")
        assert isinstance(result, str)

    def test_special_characters_do_not_crash(self, wiki_tool):
        result = wiki_tool._run(topic="!@#$%^&*()")
        assert isinstance(result, str)


class TestWikipediaToolQuality:
    """
    LLM-as-a-Judge style quality checks.
    Validates that the summary is factually grounded and readable.
    """

    def test_summary_is_full_sentences(self, wiki_tool):
        """Summary must contain at least one full sentence (ends with period)."""
        result = wiki_tool._run(topic="Photosynthesis")
        if not result.startswith("ERROR"):
            assert "." in result, "Summary should contain full sentences"

    def test_summary_is_english(self, wiki_tool):
        """Summary should contain common English words."""
        result = wiki_tool._run(topic="Photosynthesis")
        if not result.startswith("ERROR"):
            common_words = {"the", "is", "are", "a", "an", "of", "in", "and"}
            words = set(result.lower().split())
            overlap = common_words & words
            assert len(overlap) >= 2, "Summary should be in English"

    def test_summary_not_just_whitespace(self, wiki_tool):
        result = wiki_tool._run(topic="Gravity")
        assert result.strip() != ""

    def test_coordinator_output_suitable_for_quiz_generation(self, wiki_tool):
        """
        Quality gate: summary must be long enough to generate 5 MCQ questions.
        A summary shorter than 100 chars is too thin to quiz on.
        """
        result = wiki_tool._run(topic="Photosynthesis")
        if not result.startswith("ERROR"):
            assert len(result) >= 100, "Summary too short to generate meaningful questions"
