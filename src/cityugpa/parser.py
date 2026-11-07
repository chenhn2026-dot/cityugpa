"""Parsing layer: read a transcript CSV into a list of CourseRecord (owner: B).

Scope (see section B of the task breakdown):
- this layer only reads the file, converts types and validates the data, then
  returns models.CourseRecord objects;
- it does not map a grade to grade points or decide whether a grade counts
  towards the GPA -- that is D's scale.py;
- it does not truncate or average anything -- that is C's calc.py.

Input CSV (column order is free, term is optional, extra columns are ignored)::

    code,units,grade,term
    COMP1021,3,A-,2026A
    LANG1001,3,P,2026A

Normalisation:
- every field is stripped of surrounding whitespace;
- grade has all whitespace removed and is upper-cased ("a-" -> "A-"), while a
  star is preserved ("A+*" stays "A+*");
- term is stripped and upper-cased;
- units is converted to float ("3" -> 3.0).

On errors: the whole file is scanned first, then every bad row is reported at
once in a single ValueError, each message carrying its line number (line
numbers follow the physical lines of the file, so the header is line 1).

User-facing error messages stay in Chinese on purpose: the CLI output and the
demo transcript are Chinese, so all messages shown to the user are Chinese.
"""

from __future__ import annotations

import csv
import math
from collections.abc import Sequence
from pathlib import Path

from cityugpa.models import CourseRecord

__all__ = ["parse_csv"]

# term has a default value ("") in CourseRecord, so that column is optional
REQUIRED_COLUMNS = ("code", "units", "grade")
OPTIONAL_COLUMNS = ("term",)

# a broken file may have hundreds of rows; keep the error report bounded
MAX_ERRORS = 20


def parse_csv(path: str | Path) -> list[CourseRecord]:
    """Read a transcript CSV and return a list of CourseRecord.

    Args:
        path: path to the CSV file (str or Path).

    Returns:
        list[CourseRecord]: records in file order, units is always a float.

    Raises:
        FileNotFoundError: the file does not exist (E's cli turns this into
            exit code 1).
        ValueError: missing header columns, or bad rows in the body.
    """
    return _parse_file(Path(path))


def _parse_file(csv_path: Path) -> list[CourseRecord]:
    """Actual parsing flow: assumes the file is UTF-8 (BOM allowed)."""
    # utf-8-sig: CSV files saved by Excel often start with a BOM, and this
    # encoding strips the leading \ufeff automatically
    with open(csv_path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames

        if not fieldnames:
            raise ValueError(f"{csv_path} 是空文件，没有表头")

        columns = _build_column_map(fieldnames)
        # a duplicate header makes "which column to use" implicit -- fail fast
        duplicates = _duplicate_columns(fieldnames)
        if duplicates:
            raise ValueError("CSV 表头有重复列：" + ",".join(duplicates))

        # a header problem makes the whole file unreadable, so raise immediately
        # instead of scanning every row
        missing = [name for name in REQUIRED_COLUMNS if name not in columns]
        if missing:
            raise ValueError("CSV 缺少列：" + ", ".join(missing))

        records: list[CourseRecord] = []
        errors: list[str] = []
        truncated = False

        for row in reader:
            line_no = reader.line_num        # physical line number in the file
            fields = {
                name: _cell(row, columns, name)
                for name in REQUIRED_COLUMNS + OPTIONAL_COLUMNS
            }

            # blank line / all-empty row: skip it (csv skips truly empty lines,
            # but a ",,," row has to be handled here)
            if not any(fields.values()):
                continue

            # more fields than header columns means the data is misaligned;
            # fail rather than guess
            extras = row.get(None)
            if extras:
                errors.append(
                    f"第 {line_no} 行：字段比表头多"
                    f"（表头 {len(fieldnames)} 列，本行多出 {len(extras)} 个）"
                )
                continue

            row_errors: list[str] = []
            code = fields["code"]
            grade = _normalize_grade(fields["grade"])
            term = fields["term"].upper()
            units = _parse_units(fields["units"], line_no, row_errors)

            if not code:
                row_errors.append(f"第 {line_no} 行：code 为空")
            if not grade:
                row_errors.append(f"第 {line_no} 行：grade 为空")

            if row_errors:
                errors.extend(row_errors)
            else:
                records.append(CourseRecord(code=code, units=units, grade=grade, term=term))

            if len(errors) >= MAX_ERRORS:
                truncated = True
                break

    if errors:
        if truncated:
            errors.append(f"（错误太多，只报告前 {MAX_ERRORS} 条）")
        raise ValueError("\n".join(errors))

    return records


def _build_column_map(fieldnames: Sequence[str]) -> dict[str, str]:
    """Map canonical column names to the actual header names.

    Case, surrounding whitespace and a leftover BOM are ignored, so a header
    written as ``Code`` or ``UNITS`` still works after manual edits in Excel.
    """
    columns: dict[str, str] = {}
    for raw in fieldnames:
        key = raw.strip().lstrip("\ufeff").lower()
        if key and key not in columns:
            columns[key] = raw
    return columns


def _cell(row: dict, columns: dict[str, str], name: str) -> str:
    """Return one cell value; a missing column or an empty value yields ""."""
    header = columns.get(name)
    if header is None:
        return ""
    value = row.get(header)
    if value is None:
        return ""
    return value.strip()


def _normalize_grade(grade: str) -> str:
    """Normalise a grade: remove all whitespace and upper-case it, keep the star."""
    return "".join(grade.split()).upper()


def _duplicate_columns(fieldnames: Sequence[str]) -> list[str]:
    """Return header names that repeat after normalisation (case/space/BOM)."""
    normalized = [raw.strip().lstrip("\ufeff").lower() for raw in fieldnames]
    seen: set[str] = set()
    duplicates: list[str] = []
    for name in normalized:
        if name and name in seen and name not in duplicates:
            duplicates.append(name)
        seen.add(name)
    return duplicates


def _parse_units(text: str, line_no: int, errors: list[str]) -> float:
    """Convert units to float; on failure append an error and return 0.0."""
    if not text:
        errors.append(f"第 {line_no} 行：units 为空")
        return 0.0
    try:
        units = float(text)
    except ValueError:
        errors.append(f"第 {line_no} 行：units 不是数字：{text!r}")
        return 0.0
    if not math.isfinite(units) or units < 0:
        errors.append(f"第 {line_no} 行：units 必须是非负数字：{text!r}")
        return 0.0
    return units
