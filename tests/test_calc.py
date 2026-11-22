"""Tests for the SGPA / CGPA layer."""

import pytest

from cityugpa.calc import compute, cgpa, latest_attempts, plan_target, sgpa, truncate2
from cityugpa.models import CourseRecord
from cityugpa.scale import load_scale

SCALE = load_scale()


def rec(code, units, grade, term="2026A"):
    return CourseRecord(code=code, units=units, grade=grade, term=term)


def test_truncates_instead_of_rounding():
    # 3.4166... -> 3.41, a rounding calculator would say 3.42
    records = [
        rec("MA1508", 4, "A-"),
        rec("MA1503", 4, "B+"),
        rec("CS1302A", 3, "B"),
        rec("CS2613", 1, "A"),
    ]
    value, units = sgpa(records, SCALE, "2026A")
    assert units == 12
    assert value == 3.41


def test_truncate2_helper():
    assert truncate2(3.4166) == 3.41
    assert truncate2(3.9999) == 3.99
    assert truncate2(4.3) == 4.3


def test_failed_course_counts_in_the_gpa():
    records = [rec("CS1302A", 3, "C"), rec("CS2613", 3, "F")]
    value, units = sgpa(records, SCALE, "2026A")
    assert units == 6
    assert value == 1.0


def test_pass_grades_earn_units_but_stay_out_of_the_gpa():
    records = [rec("CS1302A", 3, "A"), rec("GE1401", 3, "P"), rec("GE2313", 3, "TR")]
    result = compute(records, SCALE)
    assert result.sgpa == 4.0
    assert result.gpa_units == 3
    assert result.earned_units == 9


def test_starred_grade_earns_nothing():
    records = [rec("CS1302A", 3, "A"), rec("GE2410", 3, "A+*")]
    result = compute(records, SCALE)
    assert result.sgpa == 4.0
    assert result.gpa_units == 3
    assert result.earned_units == 3


def test_retake_only_the_latest_attempt_counts():
    records = [rec("CS1302A", 3, "F"), rec("CS1302A", 3, "A")]
    unique = latest_attempts(records)
    assert len(unique) == 1
    assert unique[0].grade == "A"
    value, units = cgpa(records, SCALE)
    assert (value, units) == (4.0, 3.0)


def test_sgpa_defaults_to_the_latest_term():
    records = [rec("CS1302A", 3, "B", "2025B"), rec("CS2613", 3, "A", "2026A")]
    result = compute(records, SCALE)
    assert result.sgpa == 4.0


def test_unknown_grade_is_reported_not_silently_dropped():
    records = [rec("CS1302A", 3, "whatever")]
    with pytest.raises(ValueError):
        compute(records, SCALE)


def test_plan_target_needs_38():
    # 3.2 over 30 CU, goal 3.5 over 60 CU -> (3.5*60 - 3.2*30) / 30
    required, possible = plan_target(3.2, 30, 3.5, 30)
    assert required == pytest.approx(3.8)
    assert possible is True


def test_plan_target_reports_impossible_goals():
    required, possible = plan_target(2.0, 60, 4.3, 3)
    assert required > 4.3
    assert possible is False


def test_plan_target_without_a_cgpa_yet():
    assert plan_target(None, 0, 3.5, 15) == (None, False)
