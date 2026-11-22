# tests/test_cli.py
import sys
from unittest.mock import patch, MagicMock
from cityugpa.cli import main
from cityugpa.models import CourseRecord, GpaResult


def test_deans_list_command(capsys, monkeypatch):
    """验证 deans-list 命令存在并输出正确"""
    mock_result = GpaResult(sgpa=3.41, cgpa=3.28, gpa_units=12, earned_units=12)
    mock_records = [CourseRecord(code="COMP1021", units=3, grade="A-", term="2026A")]

    with patch("cityugpa.cli.load_scale", return_value={}), \
         patch("cityugpa.cli.parse_csv", return_value=mock_records), \
         patch("cityugpa.cli.compute", return_value=mock_result):
        monkeypatch.setattr(sys, "argv", ["cityugpa", "deans-list", "fake.csv"])
        try:
            main()
        except SystemExit as e:
            assert e.code == 0
    captured = capsys.readouterr()
    assert "Not Qualified" in captured.out


def test_target_command(capsys, monkeypatch):
    mock_result = GpaResult(sgpa=3.41, cgpa=3.28, gpa_units=54, earned_units=54)
    mock_records = [CourseRecord(code="COMP1021", units=3, grade="A-", term="2026A")]

    with patch("cityugpa.cli.load_scale", return_value={}), \
         patch("cityugpa.cli.parse_csv", return_value=mock_records), \
         patch("cityugpa.cli.compute", return_value=mock_result), \
         patch("cityugpa.cli.plan_target", return_value=(3.8, True)):
        monkeypatch.setattr(sys, "argv", ["cityugpa", "target", "--goal", "3.6", "--remaining", "15", "fake.csv"])
        try:
            main()
        except SystemExit as e:
            assert e.code == 0
    captured = capsys.readouterr()
    assert "3.80" in captured.out