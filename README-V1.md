# cityugpa

CityU GPA, computed by the rules your transcript follows.

[![PyPI](https://img.shields.io/badge/pypi-cityugpa-blue)](https://pypi.org/project/cityugpa/)
[![CI](https://github.com/chenhn2026-dot/cityugpa/actions/workflows/ci.yml/badge.svg)](https://github.com/chenhn2026-dot/cityugpa/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

```bash
git clone https://github.com/chenhn2026-dot/cityugpa
cd cityugpa
pip install -e .
cityugpa term examples/fake_transcript.csv
```

## Motivation

A generic GPA calculator gives you a different number from your transcript, because CityU does five things
differently:

| | CityU | Most calculators |
| --- | --- | --- |
| 41.0 ÷ 12 = 3.4166… | **truncate** → **3.41** | round → 3.42 |
| a course taken twice | only the latest attempt counts | both attempts count |
| a failed course (`F`) | counts as 0.0 in the average | skipped, which inflates the GPA |
| a starred grade (`A+*`) | excluded from the GPA and from earned credits | counted as `A+` |
| `P` / `TR` | earn credit, no grade points | counted as 0 points |

Source: [CityU ARRO — Course Grades](https://www.cityu.edu.hk/arro/asmt/cgrd_main.htm).

## Installation

```bash
pip install cityugpa
```

Python 3.10+. No dependencies. From a clone, `pip install -e .` works the same way.

## Usage

Four commands, one input format.

| Command | Answers |
| --- | --- |
| `cityugpa term FILE` | what is my GPA this semester |
| `cityugpa cgpa FILE` | what is my cumulative GPA |
| `cityugpa deans-list FILE` | am I on the Dean's List |
| `cityugpa target --goal 3.6 --remaining 15 FILE` | what do I need next semester |

### A semester

```bash
cityugpa term examples/fake_transcript.csv
```

```
Semester A 2026-27
MA1508       4 CU   A-      3.70
MA1503       4 CU   B+      3.30
CS1302A      3 CU   B       3.00
CS2613       1 CU   A       4.00
GE1401       3 CU   P         --
GE2313       3 CU   A+*       --

SGPA: 3.41   (12 CU in GPA, 15 CU earned)
CGPA: 3.41   (12 CU)
```

The codes are real CityU courses: MA1508 Calculus, MA1503 Linear Algebra with Applications, CS1302A Introduction
to Computer Programming, CS2613 Seminars on Contemporary Technology, GE1401 University English, GE2313 Global IT
Case Studies.

41.0 grade points over 12 CU is 3.4166…, truncated to **3.41**. A calculator that rounds shows 3.42.

`P` earns 3 CU but no grade points, which is why 15 CU are earned and only 12 CU count toward the GPA. `A+*`
counts toward neither.

### Retakes and failed courses

```bash
cityugpa cgpa examples/fake_retake.csv
```

```
All terms (latest attempt only)
CS2310       3 CU   B+      3.30
CS2613       1 CU   F       0.00
MA2185       3 CU   A-      3.70

CGPA: 3.00   (7 CU)
```

CS2310 was retaken, so only the 2026A result counts. CS2613 was failed and stays in the average at 0.0.
Counting both CS2310 attempts gives 2.79; dropping the failed course gives 3.50. Neither is what your
transcript says.

### Dean's List

```bash
cityugpa deans-list examples/fake_transcript.csv
```

```
Semester A 2026-27
SGPA: 3.41   (12 CU in GPA)
Dean's List: not eligible (SGPA 3.41 < 3.70)
```

Requires 12 CU in the term, SGPA at least 3.70, and no failed course.

### Target GPA

```bash
cityugpa target --goal 3.6 --remaining 15 examples/fake_transcript.csv
```

```
Current: 3.41 over 12 CU
Goal:    3.60 over 27 CU
Needed:  3.75 average over the next 15 CU (possible)
```

The planner starts from the CGPA it prints, so the plan matches the number on your transcript.

### The transcript file

```csv
code,units,grade,term
CS2310,3,B+,2026A
MA2185,3,A-,2026A
```

| Column | Notes |
| --- | --- |
| `code` | course code; a repeated code is a retake |
| `units` | credit units, a number |
| `grade` | `A-`, `B+`, `P`, `A+*` … |
| `term` | `2026A`, `2025B` …; used to order retakes |

UTF-8 with or without a BOM, so Excel's "CSV UTF-8" export works as-is. Blank lines are skipped and grades are
case-insensitive. A missing value or an unknown grade stops the run with the line number: a wrong number is
worse than no number.

### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | success |
| `1` | the file could not be read, or its contents are invalid |
| `2` | bad arguments |

## How it works

The CLI reads the CSV, `scale.py` turns each grade into (tenths of a grade point, counts toward GPA), `calc.py`
applies the retake rule and divides once, and `report.py` prints the result. Grade points are handled as
integers in tenths, so truncation never depends on floating-point rounding.

| Rule | Implementation | Guarded by |
| --- | --- | --- |
| Truncate, never round | integer tenths, cut at 2 decimals | `tests/test_calc.py::test_truncate_exact` |
| `F` counts as 0.0 | failed courses stay in the weighted average | `tests/test_calc.py` |
| Retakes: latest only | newest term wins, older attempts dropped from CGPA | `tests/test_calc.py` |
| Starred grades | `A+*` keeps its grade point, adds no GPA or credits | `tests/test_scale.py` |
| Non-graded marks | `P`/`TR` earn credit; `Z`/`IP`/`I`/`X`/`WD`/`AU` earn nothing | `tests/test_scale.py` |

The numbers above are pinned by `tests/test_examples.py` (3.41 and 3.00), so the documentation cannot drift
away from the code.

## Non-goals

- No AIMS connection. It does not log in, scrape, or fetch your record; you export the CSV yourself.
- No GUI. Command line only, so it runs anywhere Python runs, including JupyterHub.
- No storage. Nothing is written to disk and nothing is uploaded. The file is read, the number is printed, the
  process exits.

## Development

```bash
git clone https://github.com/chenhn2026-dot/cityugpa
cd cityugpa
python -m pip install -e .
python -m pytest -q
```

## License

MIT. See [LICENSE](LICENSE).
