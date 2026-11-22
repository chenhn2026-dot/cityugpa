"""SGPA / CGPA arithmetic under CityU's actual rules.

Takes the records the parser produced and the grade table from ``scale``.
Two rules matter more than the arithmetic itself:

* the result is **truncated** to two decimals, never rounded
* a repeated course counts once in the CGPA, using the latest attempt
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence

from cityugpa.models import CourseRecord, GpaResult
from cityugpa.scale import can_earn_credit, grade_point, load_scale

__all__ = [
    "compute",
    "plan_target",
    "truncate2",
    "latest_attempts",
    "cgpa",
    "sgpa",
]


def truncate2(value: float) -> float:
    """Cut to two decimals without rounding.

    3.4166... becomes 3.41, not 3.42. The tiny epsilon absorbs binary
    floating point error (3.2 * 100 is 320.00000000000006, 3.19 * 100 is
    318.99999999999994).
    """
    return math.floor(value * 100 + 1e-9) / 100


def _weighted_points(records: Iterable[CourseRecord], scale) -> tuple[float, float]:
    """Sum (grade point x units, units) over the courses that enter the GPA."""
    points = 0.0
    units = 0.0
    for record in records:
        point, counted = grade_point(record.grade, scale)
        if not counted or point is None or record.units <= 0:
            continue
        points += point * record.units
        units += record.units
    return points, units


def _gpa(records: Iterable[CourseRecord], scale) -> tuple[float | None, float]:
    points, units = _weighted_points(records, scale)
    if units <= 0:
        return None, 0.0
    return truncate2(points / units), units


def latest_attempts(records: Iterable[CourseRecord]) -> list[CourseRecord]:
    """One record per course code: the last attempt wins.

    CityU shows every attempt on the transcript but only the latest one
    counts towards the CGPA, so the earlier ones are dropped here.
    """
    by_code: dict[str, CourseRecord] = {}
    for record in records:
        by_code[record.code] = record
    return list(by_code.values())


def cgpa(records: Iterable[CourseRecord], scale=None) -> tuple[float | None, float]:
    """Cumulative GPA over every course, latest attempt only."""
    scale = scale if scale is not None else load_scale()
    return _gpa(latest_attempts(records), scale)


def sgpa(
    records: Iterable[CourseRecord],
    scale=None,
    term: str | None = None,
) -> tuple[float | None, float]:
    """Term GPA. Without ``term`` the latest term in the records is used."""
    scale = scale if scale is not None else load_scale()
    records = list(records)
    if term is None:
        terms = [record.term for record in records if record.term]
        term = max(terms) if terms else None
    if term is None:
        return None, 0.0
    return _gpa([record for record in records if record.term == term], scale)


def compute(
    records: Iterable[CourseRecord],
    scale=None,
    term: str | None = None,
) -> GpaResult:
    """Everything the CLI needs in one call."""
    scale = scale if scale is not None else load_scale()
    records = list(records)
    unique = latest_attempts(records)
    cgpa_value, gpa_units = _gpa(unique, scale)
    sgpa_value, _ = sgpa(records, scale, term)
    earned_units = sum(
        record.units for record in unique if can_earn_credit(record.grade, scale)
    )
    return GpaResult(
        sgpa=sgpa_value,
        cgpa=cgpa_value,
        gpa_units=gpa_units,
        earned_units=earned_units,
    )


def plan_target(
    cgpa_value: float | None,
    current_units: float,
    goal: float,
    remaining_units: float,
    max_point: float = 4.3,
) -> tuple[float | None, bool]:
    """What average the remaining units must hit to reach ``goal``.

    Returns (required grade point, whether that point exists on the scale).
    """
    if cgpa_value is None or remaining_units <= 0:
        return None, False
    have = cgpa_value * current_units
    need = goal * (current_units + remaining_units)
    required = (need - have) / remaining_units
    return required, 0 <= required <= max_point
