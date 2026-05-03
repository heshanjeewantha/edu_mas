# tests/test_grader.py
"""
Tests for the Grader agent's tool: AnswerScoringTool (Student C).

Tests cover: perfect score, zero score, partial score, invalid answers,
missing file, malformed file, answer count mismatch, and output schema.
"""
import json
import os
import pytest
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.scoring_tool import AnswerScoringTool

QUIZ_FIXTURE_PATH = "output/grader_test_quiz.json"

FIXTURE_QUIZ = [
    {"question": "Q1", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "answer": "A"},
    {"question": "Q2", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "answer": "B"},
    {"question": "Q3", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "answer": "C"},
    {"question": "Q4", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "answer": "D"},
    {"question": "Q5", "options": {"A": "a", "B": "b", "C": "c", "D": "d"}, "answer": "A"},
]


@pytest.fixture(scope="module", autouse=True)
def create_quiz_fixture():
    """Write a known quiz fixture to disk before all tests in this module."""
    os.makedirs("output", exist_ok=True)
    with open(QUIZ_FIXTURE_PATH, "w") as f:
        json.dump(FIXTURE_QUIZ, f)
    yield
    if os.path.exists(QUIZ_FIXTURE_PATH):
        os.remove(QUIZ_FIXTURE_PATH)


@pytest.fixture
def grader_tool():
    return AnswerScoringTool()


class TestAnswerScoringToolScores:
    """Tests for correct score calculation."""

    def test_perfect_score_all_correct(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B,C,D,A"
        )
        data = json.loads(result)
        assert data["score_percentage"] == 100.0

    def test_zero_score_all_wrong(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="B,C,D,A,B"
        )
        data = json.loads(result)
        assert data["score_percentage"] == 0.0

    def test_partial_score_three_correct(self, grader_tool):
        # Correct: A,B,C — Wrong: A(for D), B(for A)
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B,C,A,B"
        )
        data = json.loads(result)
        assert data["correct_count"] == 3
        assert data["score_percentage"] == 60.0

    def test_score_percentage_is_float(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B,C,D,A"
        )
        data = json.loads(result)
        assert isinstance(data["score_percentage"], float)

    def test_score_between_0_and_100(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B,C,D,A"
        )
        data = json.loads(result)
        assert 0.0 <= data["score_percentage"] <= 100.0


class TestAnswerScoringToolOutputSchema:
    """Tests for correct output structure."""

    def test_result_is_valid_json(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B,C,D,A"
        )
        data = json.loads(result)  # must not raise
        assert data is not None

    def test_result_has_required_keys(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B,C,D,A"
        )
        data = json.loads(result)
        assert "results" in data
        assert "score_percentage" in data
        assert "correct_count" in data
        assert "total_questions" in data

    def test_results_list_length_matches_quiz(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B,C,D,A"
        )
        data = json.loads(result)
        assert len(data["results"]) == 5

    def test_each_result_entry_has_required_keys(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B,C,D,A"
        )
        data = json.loads(result)
        for r in data["results"]:
            assert "question_no" in r
            assert "student_answer" in r
            assert "correct_answer" in r
            assert "is_correct" in r

    def test_is_correct_is_boolean(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B,C,D,A"
        )
        data = json.loads(result)
        for r in data["results"]:
            assert isinstance(r["is_correct"], bool)


class TestAnswerScoringToolNegative:
    """Error-handling and edge case tests."""

    def test_missing_quiz_file_returns_error(self, grader_tool):
        result = grader_tool._run(
            quiz_path="output/nonexistent_quiz.json",
            student_answers="A,B,C,D,A"
        )
        assert result.startswith("ERROR")

    def test_answers_uppercased_automatically(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="a,b,c,d,a"
        )
        data = json.loads(result)
        assert data["score_percentage"] == 100.0

    def test_answers_with_spaces_are_stripped(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers=" A , B , C , D , A "
        )
        data = json.loads(result)
        assert data["score_percentage"] == 100.0

    def test_invalid_answer_letter_marked_invalid(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="X,B,C,D,A"
        )
        data = json.loads(result)
        assert data["results"][0]["student_answer"] == "INVALID"

    def test_fewer_answers_than_questions_handled(self, grader_tool):
        result = grader_tool._run(
            quiz_path=QUIZ_FIXTURE_PATH,
            student_answers="A,B"
        )
        data = json.loads(result)
        assert len(data["results"]) == 5
