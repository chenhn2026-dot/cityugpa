from dataclasses import dataclass

@dataclass(frozen=True)
class CourseRecord:
    code: str
    units: float
    grade: str
    term: str = ""

@dataclass(frozen=True)
class GpaResult:
    sgpa: float | None
    cgpa: float | None
    gpa_units: float
    earned_units: float
