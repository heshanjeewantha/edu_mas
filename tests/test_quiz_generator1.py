# tests/test_quiz_generator.py
"""
Tests for the Quiz Generator agent's tool: SaveQuizTool (Student B).

Tests cover: valid save, malformed JSON, empty array, missing keys,
file creation verification, and schema structure validation.
"""
import json
import os
import pytest
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.file_tools import SaveQuizTool

SAMPLE_QUIZ = [
    {
        "question": "What is the primary input for photosynthesis?",
        "options": {"A": "Oxygen", "B": "Carbon dioxide", "C": "Nitrogen", "D": "Hydrogen"},
        "answer": "B",
    },
    {
        "question": "What pigment captures light in plants?",
        "options": {"A": "Melanin", "B": "Carotene", "C": "Chlorophyll", "D": "Anthocyanin"},
        "answer": "C",
    },
    {
        "question": "Where does photosynthesis take place?",
        "options": {"A": "Mitochondria", "B": "Nucleus", "C": "Ribosome", "D": "Chloroplast"},
        "answer": "D",
    },
    {
        "question": "What gas is released during photosynthesis?",
        "options": {"A": "CO2", "B": "N2", "C": "O2", "D": "H2"},
        "answer": "C",
    },
    {
        "question": "What is the energy source for photosynthesis?",
        "options": {"A": "Heat", "B": "Sunlight", "C": "Wind", "D": "Water"},
        "answer": "B",
    },
]

OUTPUT_DIR = "output"


@pytest.fixture
def save_tool():
    return SaveQuizTool()


@pytest.fixture(autouse=True)
def cleanup():
    """Remove test output files after each test."""
    yield
    for fname in os.listdir(OUTPUT_DIR) if os.path.exists(OUTPUT_DIR) else []:
        if fname.startswith("test_") or fname.startswith("struct_") or fname.startswith("five_"):
            os.remove(os.path.join(OUTPUT_DIR, fname))


class TestSaveQuizToolPositive:
    """Happy-path tests for valid quiz saving."""

    def test_saves_valid_quiz_returns_success(self, save_tool):
        result = save_tool._run(quiz_json=json.dumps(SAMPLE_QUIZ), filename="test_quiz.json")
        assert "SUCCESS" in result

    def test_output_file_is_created(self, save_tool):
        save_tool._run(quiz_json=json.dumps(SAMPLE_QUIZ), filename="test_created.json")
        assert os.path.exists("output/test_created.json")

    def test_saved_file_is_valid_json(self, save_tool):
        save_tool._run(quiz_json=json.dumps(SAMPLE_QUIZ), filename="test_valid.json")
        with open("output/test_valid.json") as f:
            data = json.load(f)
        assert isinstance(data, list)

    def test_saved_quiz_has_five_questions(self, save_tool):
        save_tool._run(quiz_json=json.dumps(SAMPLE_QUIZ), filename="five_q.json")
        with open("output/five_q.json") as f:
            data = json.load(f)
        assert len(data) == 5

    def test_each_question_has_required_keys(self, save_tool):
        save_tool._run(quiz_json=json.dumps(SAMPLE_QUIZ), filename="struct_test.json")
        with open("output/struct_test.json") as f:
            data = json.load(f)
        for q in data:
            assert "question" in q
            assert "options" in q
            assert "answer" in q

    def test_each_question_has_four_options(self, save_tool):
        save_tool._run(quiz_json=json.dumps(SAMPLE_QUIZ), filename="struct_opts.json")
        with open("output/struct_opts.json") as f:
            data = json.load(f)
        for q in data:
            assert len(q["options"]) == 4
            assert set(q["options"].keys()) == {"A", "B", "C", "D"}

    def test_answer_key_is_valid_choice(self, save_tool):
        save_tool._run(quiz_json=json.dumps(SAMPLE_QUIZ), filename="struct_ans.json")
        with open("output/struct_ans.json") as f:
            data = json.load(f)
        for q in data:
            assert q["answer"] in {"A", "B", "C", "D"}


class TestSaveQuizToolNegative:
    """Error-handling tests for invalid inputs."""

    def test_rejects_invalid_json_string(self, save_tool):
        result = save_tool._run(quiz_json="NOT VALID JSON", filename="test_bad.json")
        assert "ERROR" in result

    def test_rejects_json_object_not_array(self, save_tool):
        result = save_tool._run(quiz_json='{"question": "test"}', filename="test_obj.json")
        assert "ERROR" in result

    def test_rejects_empty_array(self, save_tool):
        result = save_tool._run(quiz_json="[]", filename="test_empty.json")
        assert "ERROR" in result

    def test_rejects_question_missing_answer_key(self, save_tool):
        bad_quiz = [{"question": "What?", "options": {"A": "1", "B": "2", "C": "3", "D": "4"}}]
        result = save_tool._run(quiz_json=json.dumps(bad_quiz), filename="test_missing.json")
        assert "ERROR" in result

    def test_does_not_create_file_on_bad_json(self, save_tool):
        save_tool._run(quiz_json="BROKEN", filename="test_nocreate.json")
        assert not os.path.exists("output/test_nocreate.json")
