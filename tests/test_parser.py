"""Tests for the parsing layer (owner: B).

Covers the acceptance points of section B of the task breakdown:
1. a normal file yields 4 records;
2. a missing header column -> ValueError whose message names the column;
3. a non-numeric units value -> ValueError whose message carries the line number.

Empty grades, lower-case grades, BOM, blank lines and error aggregation are
covered as well.

Note: user-facing error messages are in Chinese (same language as the CLI
output), so assertions on message text match Chinese substrings.
"""

from pathlib import Path

import pytest

from cityugpa.models import CourseRecord
from cityugpa.parser import parse_csv

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
HEADER = "code,units,grade,term\n"


def write_csv(path: Path, text: str, encoding: str = "utf-8") -> str:
    """Write the given content to a temporary CSV and return its path as str
    (parse_csv must accept str)."""
    path.write_text(text, encoding=encoding)
    return str(path)


# ---------------------------------------------------------------- happy path

def test_parse_ok(tmp_path):
    """A normal file: 4 records, correct values and types."""
    path = write_csv(
        tmp_path / "a.csv",
        HEADER + "COMP1021,3,A-,2026A\n"
                 "MATH1011,3,B+,2026A\n"
                 "GE1401,3,B,2026A\n"
                 "LANG1001,3,P,2026A\n",
    )

    records = parse_csv(path)

    assert len(records) == 4
    assert all(isinstance(r, CourseRecord) for r in records)
    assert records[0] == CourseRecord(code="COMP1021", units=3.0, grade="A-", term="2026A")
    assert records[3].grade == "P"


def test_units_is_float_not_str(tmp_path):
    """units must be a float, otherwise the GPA calculation cannot use it."""
    path = write_csv(tmp_path / "b.csv", HEADER + "COMP1021,3,A-,2026A\n")

    record = parse_csv(path)[0]

    assert record.units == 3.0
    assert isinstance(record.units, float)


def test_parse_retake_example_keeps_every_row(tmp_path):
    """A retake file: both rows are kept; keeping only the latest one is
    C's job in calc.py."""
    path = write_csv(
        tmp_path / "c.csv",
        HEADER + "COMP1021,3,F,2025A\nCOMP1021,3,B+,2026A\n",
    )

    records = parse_csv(path)

    assert len(records) == 2
    assert [r.grade for r in records] == ["F", "B+"]


@pytest.mark.parametrize("filename", ["fake_transcript.csv", "fake_retake.csv"])
def test_parse_examples_from_repo(filename):
    """Read the example files F keeps in examples/ (B's first acceptance item)."""
    path = EXAMPLES / filename
    if not path.exists():          # F's commit has not been pulled yet
        pytest.skip(f"examples/{filename} has not been committed yet")

    records = parse_csv(path)

    assert records, "example file must not be empty"
    assert all(r.units > 0 and r.grade for r in records)


def test_term_column_optional(tmp_path):
    """The term column may be missing: CourseRecord.term falls back to ""."""
    path = write_csv(tmp_path / "d.csv", "code,units,grade\nCOMP1021,3,A-\n")

    record = parse_csv(path)[0]

    assert record.term == ""


def test_extra_columns_ignored(tmp_path):
    """Extra columns (e.g. note) are ignored and do not affect parsing."""
    path = write_csv(tmp_path / "e.csv", "code,units,grade,term,note\nCOMP1021,3,A-,2026A,重修\n")

    record = parse_csv(path)[0]

    assert record == CourseRecord(code="COMP1021", units=3.0, grade="A-", term="2026A")


def test_column_order_and_case_tolerated(tmp_path):
    """Any column order and any header case are accepted."""
    path = write_csv(tmp_path / "f.csv", "Units,Grade,Term,Code\n3,A-,2026A,COMP1021\n")

    record = parse_csv(path)[0]

    assert record == CourseRecord(code="COMP1021", units=3.0, grade="A-", term="2026A")


def test_grade_is_uppercased(tmp_path):
    """The lower-case grade a- becomes A-."""
    path = write_csv(tmp_path / "g.csv", HEADER + "COMP1021,3,a-,2026a\n")

    record = parse_csv(path)[0]

    assert record.grade == "A-"
    assert record.term == "2026A"


def test_star_grade_is_kept_as_is(tmp_path):
    """A starred grade is passed through unchanged (deciding whether to exclude
    it is D's job, not the parser's)."""
    path = write_csv(tmp_path / "h.csv", HEADER + "GE1401,3, a+* ,2026A\n")

    assert parse_csv(path)[0].grade == "A+*"


def test_bom_file(tmp_path):
    """A CSV saved by Excel carries a BOM; reading it with utf-8-sig must work."""
    path = write_csv(tmp_path / "i.csv", HEADER + "COMP1021,3,A-,2026A\n", encoding="utf-8-sig")

    assert len(parse_csv(path)) == 1


def test_blank_lines_skipped(tmp_path):
    """Blank lines and all-comma rows are skipped, not treated as errors."""
    path = write_csv(
        tmp_path / "j.csv",
        HEADER + "\n"                  # truly blank line
                 "COMP1021,3,A-,2026A\n"
                 ",,,\n"               # all fields empty
                 "\n"
                 "MATH1011,3,B+,2026A\n",
    )

    assert len(parse_csv(path)) == 2


# ---------------------------------------------------------------- error path

def test_missing_column(tmp_path):
    """A missing units column -> ValueError whose message names units."""
    path = write_csv(tmp_path / "k.csv", "code,grade\nCOMP1021,A-\n")

    with pytest.raises(ValueError, match="units"):
        parse_csv(path)


def test_missing_column_lists_all_missing(tmp_path):
    """When two columns are missing, both are reported."""
    path = write_csv(tmp_path / "l.csv", "code\nCOMP1021\n")

    with pytest.raises(ValueError) as excinfo:
        parse_csv(path)

    assert "units" in str(excinfo.value)
    assert "grade" in str(excinfo.value)


def test_units_not_a_number(tmp_path):
    """A non-numeric units value -> error that carries the line number (the
    header is line 1, so data starts at line 2)."""
    path = write_csv(tmp_path / "m.csv", HEADER + "COMP1021,三分,A-,2026A\n")

    with pytest.raises(ValueError) as excinfo:
        parse_csv(path)

    message = str(excinfo.value)
    assert "units" in message
    assert "第 2 行" in message


def test_grade_empty(tmp_path):
    """An empty grade -> error that carries the line number."""
    path = write_csv(
        tmp_path / "n.csv",
        HEADER + "COMP1021,3,A-,2026A\n"
                 "MATH1011,3,,2026A\n",
    )

    with pytest.raises(ValueError) as excinfo:
        parse_csv(path)

    message = str(excinfo.value)
    assert "grade" in message
    assert "第 3 行" in message


def test_code_empty(tmp_path):
    """An empty code -> error that carries the line number."""
    path = write_csv(tmp_path / "o.csv", HEADER + ",3,A-,2026A\n")

    with pytest.raises(ValueError, match="code"):
        parse_csv(path)


def test_negative_units_rejected(tmp_path):
    """Units cannot be negative."""
    path = write_csv(tmp_path / "p.csv", HEADER + "COMP1021,-3,A-,2026A\n")

    with pytest.raises(ValueError, match="units"):
        parse_csv(path)


def test_errors_from_multiple_rows_are_collected(tmp_path):
    """Errors are collected and raised together instead of stopping at the
    first bad row."""
    path = write_csv(
        tmp_path / "q.csv",
        HEADER + "COMP1021,abc,A-,2026A\n"   # line 2: bad units
                 "MATH1011,3,A-,2026A\n"     # line 3: fine
                 "GE1401,3,,2026A\n",        # line 4: empty grade
    )

    with pytest.raises(ValueError) as excinfo:
        parse_csv(path)

    message = str(excinfo.value)
    assert "第 2 行" in message
    assert "第 4 行" in message
    assert "第 3 行" not in message


def test_extra_fields_row_is_error(tmp_path):
    """A row with more fields than the header means misaligned data -> error."""
    path = write_csv(tmp_path / "r.csv", HEADER + "COMP1021,3,A-,2026A,多出来一列\n")

    with pytest.raises(ValueError, match="字段比表头多"):
        parse_csv(path)


def test_empty_file(tmp_path):
    """An empty file raises instead of silently returning an empty list."""
    path = write_csv(tmp_path / "s.csv", "")

    with pytest.raises(ValueError, match="表头"):
        parse_csv(path)


def test_missing_file(tmp_path):
    """A missing file -> FileNotFoundError (E's cli maps it to exit code 1)."""
    with pytest.raises(FileNotFoundError):
        parse_csv(tmp_path / "不存在.csv")


def test_duplicate_column_rejected(tmp_path):
    """Duplicate header columns -> error, so that "which column wins" never
    becomes an implicit rule."""
    path = write_csv(tmp_path / "t.csv", "code,units,grade,grade\nCOMP1021,3,A-,B+\n")

    with pytest.raises(ValueError, match="重复列.*grade"):
        parse_csv(path)


def test_non_utf8_file_gets_friendly_error(tmp_path):
    """A GBK file (what Excel saves by default on Chinese Windows) -> a hint to
    save it as CSV UTF-8 instead of a raw decoding error."""
    path = tmp_path / "gbk.csv"
    path.write_bytes("code,units,grade,term,备注\nCOMP1021,3,A-,2026A,重修\n".encode("gbk"))

    with pytest.raises(ValueError) as excinfo:
        parse_csv(str(path))

    message = str(excinfo.value)
    assert "另存为" in message
    assert "UTF-8" in message


def test_crlf_line_endings(tmp_path):
    """CRLF line endings (Windows / Excel) must parse correctly."""
    path = tmp_path / "crlf.csv"
    path.write_bytes(b"code,units,grade,term\r\nCOMP1021,3,A-,2026A\r\n")

    assert len(parse_csv(str(path))) == 1


def test_header_only_returns_empty_list(tmp_path):
    """A header without any data row -> empty list (not an error; C decides
    whether the SGPA is None)."""
    path = write_csv(tmp_path / "u.csv", HEADER)

    assert parse_csv(path) == []
