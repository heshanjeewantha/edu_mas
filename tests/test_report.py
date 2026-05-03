# tests/test_report_writer.py
"""
Tests for the Report Writer agent's tool: WriteReportTool (Student D).

Tests cover: successful report creation, JSON validity, required schema keys,
pass/fail threshold logic, malformed score input, and file naming convention.
"""
import json
import os
import glob
import pytest
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools.report_tool import WriteReportTool

SAMPLE_SCORE_JSON = json.dumps({
    "results": [
        {"question_no": 1, "question": "Q1?", "student_answer": "A", "correct_answer": "A", "is_correct": True},
        {"question_no": 2, "question": "Q2?", "student_answer": "B", "correct_answer": "B", "is_correct": True},
        {"question_no": 3, "question": "Q3?", "student_answer": "A", "correct_answer": "C", "is_correct": False},
        {"question_no": 4, "question": "Q4?", "student_answer": "D", "correct_answer": "D", "is_correct": True},
        {"question_no": 5, "question": "Q5?", "student_answer": "B", "correct_answer": "A", "is_correct": False},
    ],
    "correct_count": 3,
    "total_questions": 5,
    "score_percentage": 60.0,
})

FAIL_SCORE_JSON = json.dumps({
    "results": [
        {"question_no": i+1, "question": f"Q{i+1}?", "student_answer": "A",
         "correct_answer": "D", "is_correct": False} for i in range(5)
    ],
    "correct_count": 0,
    "total_questions": 5,
    "score_percentage": 0.0,
})


@pytest.fixture
def report_tool():
    return WriteReportTool()


@pytest.fixture(autouse=True)
def cleanup_reports():
    """Remove generated test reports after each test."""
    yield
    for f in glob.glob("output/report_*.json"):
        try:
            os.remove(f)
        except Exception:
            pass


class TestWriteReportToolPositive:
    """Happy-path tests for valid report generation."""

    def test_returns_success_message(self, report_tool):
        result = report_tool._run(
            topic="Photosynthesis",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice",
            difficulty="medium"
        )
        assert "SUCCESS" in result

    def test_report_file_is_created(self, report_tool):
        report_tool._run(
            topic="Photosynthesis",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice"
        )
        reports = glob.glob("output/report_*.json")
        assert len(reports) >= 1

    def test_report_is_valid_json(self, report_tool):
        report_tool._run(
            topic="Photosynthesis",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice"
        )
        report_file = sorted(glob.glob("output/report_*.json"))[-1]
        with open(report_file) as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_report_has_required_top_level_keys(self, report_tool):
        report_tool._run(
            topic="Photosynthesis",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice"
        )
        report_file = sorted(glob.glob("output/report_*.json"))[-1]
        with open(report_file) as f:
            data = json.load(f)
        assert "report_metadata" in data
        assert "student" in data
        assert "results" in data
        assert "question_feedback" in data

    def test_student_name_in_report(self, report_tool):
        report_tool._run(
            topic="Gravity",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Bob"
        )
        report_file = sorted(glob.glob("output/report_*.json"))[-1]
        with open(report_file) as f:
            data = json.load(f)
        assert data["student"]["name"] == "Bob"

    def test_topic_in_report(self, report_tool):
        report_tool._run(
            topic="Gravity",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice"
        )
        report_file = sorted(glob.glob("output/report_*.json"))[-1]
        with open(report_file) as f:
            data = json.load(f)
        assert data["student"]["topic"] == "Gravity"

    def test_score_percentage_correct(self, report_tool):
        report_tool._run(
            topic="Photosynthesis",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice"
        )
        report_file = sorted(glob.glob("output/report_*.json"))[-1]
        with open(report_file) as f:
            data = json.load(f)
        assert data["results"]["score_percentage"] == 60.0

    def test_question_feedback_has_five_entries(self, report_tool):
        report_tool._run(
            topic="Photosynthesis",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice"
        )
        report_file = sorted(glob.glob("output/report_*.json"))[-1]
        with open(report_file) as f:
            data = json.load(f)
        assert len(data["question_feedback"]) == 5


class TestWriteReportToolPassFail:
    """Tests for pass/fail threshold logic (60% threshold)."""

    def test_score_60_percent_is_pass(self, report_tool):
        report_tool._run(
            topic="Test",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice"
        )
        report_file = sorted(glob.glob("output/report_*.json"))[-1]
        with open(report_file) as f:
            data = json.load(f)
        assert data["results"]["pass_status"] == "PASS"

    def test_score_0_percent_is_fail(self, report_tool):
        report_tool._run(
            topic="Test",
            score_json=FAIL_SCORE_JSON,
            student_name="Alice"
        )
        report_file = sorted(glob.glob("output/report_*.json"))[-1]
        with open(report_file) as f:
            data = json.load(f)
        assert data["results"]["pass_status"] == "FAIL"

    def test_pass_threshold_recorded_in_report(self, report_tool):
        report_tool._run(
            topic="Test",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice"
        )
        report_file = sorted(glob.glob("output/report_*.json"))[-1]
        with open(report_file) as f:
            data = json.load(f)
        assert data["results"]["pass_threshold_percent"] == 60


class TestWriteReportToolNegative:
    """Error-handling tests for bad inputs."""

    def test_invalid_score_json_returns_error(self, report_tool):
        result = report_tool._run(
            topic="Gravity",
            score_json="NOT JSON",
            student_name="Alice"
        )
        assert "ERROR" in result

    def test_empty_score_json_returns_error(self, report_tool):
        result = report_tool._run(
            topic="Gravity",
            score_json="",
            student_name="Alice"
        )
        assert "ERROR" in result

    def test_report_filename_has_timestamp_format(self, report_tool):
        report_tool._run(
            topic="Photosynthesis",
            score_json=SAMPLE_SCORE_JSON,
            student_name="Alice"
        )
        reports = glob.glob("output/report_*.json")
        assert len(reports) >= 1
        fname = os.path.basename(sorted(reports)[-1])
        assert fname.startswith("report_")
        assert fname.endswith(".json")
        # filename format: report_YYYYMMDD_HHMMSS.json
        parts = fname.replace("report_", "").replace(".json", "").split("_")
        assert len(parts) == 2
        assert len(parts[0]) == 8  # YYYYMMDD
        assert len(parts[1]) == 6  # HHMMSS
