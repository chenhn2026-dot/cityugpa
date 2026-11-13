# cityugpa

CityU GPA, computed by the rules your transcript follows.

[![PyPI](https://img.shields.io/badge/pypi-cityugpa-blue)](https://pypi.org/project/cityugpa/)
[![CI](https://github.com/chenhn2026-dot/cityugpa/actions/workflows/ci.yml/badge.svg)](https://github.com/chenhn2026-dot/cityugpa/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**In a hurry?** Install it with `pip install cityugpa`, then run `cityugpa term my_grades.csv`.

**Never used a terminal before?** Skip that line and read [Installation](#installation). It explains every
step, including how to open the terminal and how to check that Python is already on your computer.

---

## Contents

1. [What it does](#what-it-does)
2. [Words you will see](#words-you-will-see)
3. [Motivation](#motivation)
4. [Installation](#installation)
5. [Usage](#usage)
6. [How it works](#how-it-works)
7. [Non-goals](#non-goals)
8. [Development](#development)

## What it does

You give it one file: a plain table of your courses and grades. It gives you back the GPA that CityU would
calculate, and it shows you how it got there, line by line.

That is the whole idea. There is no login, no screenshot to upload, and nothing is sent anywhere.

Here is a real run. Six courses, four of which count toward the GPA:

```
Semester A 2026-27
MA1508       4 CU   A-      3.70
MA1503       4 CU   B+      3.30
CS1302A      3 CU   B       3.00
CS2613       1 CU   A       4.00
GE1401       3 CU   P         --
GE2313       3 CU   A+*       --

SGPA: 3.41   (12 CU in GPA, 15 CU earned)
```

The useful part is not the 3.41. It is the two lines underneath the table: `P` earned you 3 credits but no
grade points, and `A+*` earned you neither. Most calculators get those two lines wrong, and that is how you
end up with 3.42 instead of 3.41.

## Words you will see

If any of these are new, read this table once and the rest of the page will make sense.

| Word | What it means |
| --- | --- |
| **Terminal** | The window where you type commands instead of clicking. On macOS it is called Terminal; on Windows, PowerShell. |
| **Python** | The programming language this tool is written in. You need version 3.10 or newer installed. |
| **pip** | The program that downloads and installs Python packages. It comes with Python. |
| **Package** | A bundle of code you can install. `cityugpa` is one. |
| **Command** | A line of text you type into the terminal and run by pressing Enter. |
| **CSV** | A plain text file where each row is a record and commas separate the values. Excel can save one. |
| **CU / credit unit** | How much a course is worth. Most CityU courses are 3 CU; some are 1, 4 or 6. |
| **Grade point** | The number behind a letter grade. At CityU, `A+` = 4.3, `A` = 4.0, `A-` = 3.7, and `F` = 0.0. |
| **SGPA** | Semester GPA: the average for one term. |
| **CGPA** | Cumulative GPA: the average across every term so far. |
| **Retake** | Taking the same course twice. The transcript shows both attempts; the CGPA uses only the latest. |
| **Starred grade** | A grade written with `*`, such as `A+*`. It appears on the transcript but is left out of the GPA. |
| **Dean's List** | An honour list. At CityU you need 12 CU in the term, SGPA of at least 3.70, and no failed course. |

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

The rules come from [CityU ARRO — Course Grades](https://www.cityu.edu.hk/arro/asmt/cgrd_main.htm). Everything
this tool does is one of those five rules, or a direct consequence of them.

## Installation

This takes about three minutes. You will type three short commands and check one result.

### Step 1. Open a terminal

- **macOS**: press `Command` + `Space`, type `Terminal`, press Enter.
- **Windows**: press the Windows key, type `PowerShell`, press Enter.
- **Linux**: press `Ctrl` + `Alt` + `T`.

A window opens with a line of text ending in `$` or `>`. That is called the prompt. You type after it.

### Step 2. Check that Python is installed

Type this and press Enter:

```bash
python3 --version
```

You should see something like `Python 3.12.4`. Any number from **3.10** upwards works.

If you see an error such as `command not found`, or a version below 3.10:

- macOS: install it from [python.org/downloads](https://www.python.org/downloads/), or run `brew install python`
  if you already use Homebrew.
- Windows: install it from [python.org/downloads](https://www.python.org/downloads/) and tick
  **"Add python.exe to PATH"** on the first screen of the installer.

On Windows the command is usually `python` rather than `python3`. If `python3` fails, try `python --version`.

### Step 3. Install the package

```bash
pip install cityugpa
```

If `pip` is not recognised, use the form that always works:

```bash
python3 -m pip install cityugpa
```

You should see a few lines ending in something like:

```
Successfully installed cityugpa-0.1.0
```

> **Just downloaded the code instead?** If you have the project folder (a clone, or a ZIP from GitHub) and the
> package is not on PyPI yet, run `pip install .` from inside that folder instead.

### Step 4. Check that it worked

```bash
cityugpa --help
```

You should see a usage message listing `term`, `cgpa`, `deans-list` and `target`. That means the command is
installed and on your PATH.

If you get `command not found: cityugpa`, Python installed the library but the launcher is not on your PATH.
Use `python3 -m cityugpa --help` instead. It is the same program, and it always works.

### Step 5. If something goes wrong

| Message you see | What it means | What to do |
| --- | --- | --- |
| `command not found: python3` | Python is not installed, or not on PATH | Install from python.org (Step 2) |
| `command not found: pip` | pip is missing from PATH | Use `python3 -m pip install cityugpa` |
| `Could not find a version that satisfies the requirement cityugpa` | The release is not on PyPI yet, or you are in a folder with a broken `pyproject.toml` | Install from the project folder with `pip install .` |
| `error: externally-managed-environment` | Your system Python protects itself | Create a virtual environment, or run `pip install --user cityugpa` |
| `Permission denied` | You are installing into a folder you do not own | Add `--user`, or use a virtual environment |
| `SSL: CERTIFICATE_VERIFY_FAILED` | A network proxy or old certificates | Try another network, or ask your lab administrator |

### Optional: keep it separate from the rest of your system

A virtual environment is a private folder for one project. It is not required, but it prevents conflicts:

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install cityugpa
```

To leave it later, type `deactivate`.

## Usage

Every command needs one thing: a CSV file with your courses. If you do not have one yet, make it now. It takes
two minutes and you can delete it afterwards.

### Step 1. Make your transcript file

A CSV is just a table in a text file. The first row names the columns, and every row after it is one course
attempt.

Create a file called `my_grades.csv` and paste exactly this into it:

```csv
code,units,grade,term
MA1508,4,A-,2026A
MA1503,4,B+,2026A
CS1302A,3,B,2026A
CS2613,1,A,2026A
GE1401,3,P,2026A
GE2313,3,A+*,2026A
```

Save it as plain text, not as a Word document.

- **Excel**: File → Save As → choose **CSV UTF-8 (Comma delimited)**.
- **TextEdit (macOS)**: Format → Make Plain Text, then save with the name `my_grades.csv`.
- **Notepad (Windows)**: Save As, set Encoding to **UTF-8**, name it `my_grades.csv`.

The four columns:

| Column | What goes in it | Example |
| --- | --- | --- |
| `code` | the course code, exactly as it appears on the transcript | `MA1508` |
| `units` | the credit units, as a number | `4` |
| `grade` | the letter grade, including any `*` | `A-`, `P`, `A+*` |
| `term` | the term, written as year + letter | `2026A` |

Things that are fine:

- One row per attempt, so a retaken course appears twice with different terms.
- Capital or small letters for grades; `a-` is read as `A-`.
- A UTF-8 BOM, which is what Excel adds automatically.
- Blank lines, which are skipped.

Things that stop the run:

- A missing value, such as an empty grade.
- A grade that is not in the CityU scale, such as `B++`.
- A `units` value that is not a number, such as `three`.

When that happens the tool tells you the line number and stops, because a silent wrong number is worse than an
error message.

### Step 2. Calculate your semester GPA

Put `my_grades.csv` in the folder you are in, then run:

```bash
cityugpa term my_grades.csv
```

You should see exactly this:

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

**How to read it, column by column:**

| Column | Meaning |
| --- | --- |
| `MA1508` | the course code |
| `4 CU` | the course is worth 4 credit units |
| `A-` | your grade |
| `3.70` | the grade point for `A-` |
| `--` | this course does not count toward the GPA |

**How to read the two summary lines:**

- `SGPA: 3.41` is the average for this term.
- `(12 CU in GPA, 15 CU earned)` means 12 credit units went into the calculation, while 15 units were earned
  in total. The difference is `GE1401` (`P`): it earns credit but has no grade point, so it cannot be in the
  average. `GE2313` (`A+*`) is excluded completely, so it adds nothing to either number.
- `CGPA: 3.41` is the cumulative average. Your file only has one term, so it equals the SGPA.

**Why 3.41 and not 3.42?** Add up each grade point multiplied by its credit units:

```
4 × 3.70 = 14.8
4 × 3.30 = 13.2
3 × 3.00 =  9.0
1 × 4.00 =  4.0
             ----
             41.0   grade points
```

Then divide by the 12 units that count: 41.0 ÷ 12 = 3.4166… CityU cuts the number at two decimals instead of
rounding, so the answer is **3.41**. A calculator that rounds gives 3.42.

### Step 3. Calculate your CGPA, including retakes

Make a second file called `my_retakes.csv`:

```csv
code,units,grade,term
CS2310,3,C+,2025A
CS2310,3,B+,2026A
CS2613,1,F,2026A
MA2185,3,A-,2026A
```

Then run:

```bash
cityugpa cgpa my_retakes.csv
```

```
All terms (latest attempt only)
CS2310       3 CU   B+      3.30
CS2613       1 CU   F       0.00
MA2185       3 CU   A-      3.70

CGPA: 3.00   (7 CU)
```

Two things are happening here:

- `CS2310` appears twice. Only the 2026A attempt counts, so the `C+` from 2025A is dropped.
- `CS2613` was failed. It still counts, with 0.0 grade points, and it stays in the 7 units.

If you counted both `CS2310` attempts you would get 2.79. If you dropped the failed course you would get 3.50.
Neither is what your transcript says.

### Step 4. Check the Dean's List

```bash
cityugpa deans-list my_grades.csv
```

```
Semester A 2026-27
SGPA: 3.41   (12 CU in GPA)
Dean's List: not eligible (SGPA 3.41 < 3.70)
```

The tool tells you which condition failed, not just "no". The conditions are 12 CU in the term, an SGPA of at
least 3.70, and no failed course.

### Step 5. Find out what you need next semester

```bash
cityugpa target --goal 3.6 --remaining 15 my_grades.csv
```

```
Current: 3.41 over 12 CU
Goal:    3.60 over 27 CU
Needed:  3.75 average over the next 15 CU (possible)
```

Read it as: you have a 3.41 CGPA over 12 units. To reach 3.60 after another 15 units, you need to average 3.75
in those 15 units. `(possible)` means that average is inside the 4.3 scale.

The planner starts from the CGPA the tool prints, so the plan matches the number you can see, not a hidden
unrounded value.

### Exit codes

Scripts use these, and so can you:

| Code | Meaning |
| --- | --- |
| `0` | everything worked |
| `1` | the file could not be read, or its contents are invalid |
| `2` | the arguments were wrong |

## How it works

Four small modules and one JSON file:

```
your CSV → parser.py → scale.py → calc.py → report.py → your terminal
             read        grade →     retake +     aligned
             rows        points      average      table
```

- `parser.py` reads the CSV and reports problems with line numbers.
- `scale.py` turns a grade string such as `A-` into `(3.7, counts toward GPA)`.
- `calc.py` applies the retake rule and divides once.
- `report.py` prints the table.

Grade points are stored as integers in tenths (4.3 becomes 43), so the division and the truncation never depend
on floating-point rounding. That is why the answer is exactly 3.41 and not occasionally 3.40.

### The five rules, and the test that guards each one

| Rule | Implementation | Guarded by |
| --- | --- | --- |
| Truncate, never round | integer tenths, cut at 2 decimals | `tests/test_calc.py::test_truncate_exact` |
| `F` counts as 0.0 | failed courses stay in the weighted average | `tests/test_calc.py` |
| Retakes: latest only | newest term wins, older attempts dropped from CGPA | `tests/test_calc.py` |
| Starred grades | `A+*` keeps its grade point, adds no GPA or credits | `tests/test_scale.py` |
| Non-graded marks | `P`/`TR` earn credit; `Z`/`IP`/`I`/`X`/`WD`/`AU` earn nothing | `tests/test_scale.py` |

The two example files above are also a test: `tests/test_examples.py` asserts that they produce 3.41 and 3.00.
If a rule changes and the numbers move, the test fails before the documentation can become a lie.

## Non-goals

- **No AIMS connection.** It does not log in, scrape, or fetch your record. You export the CSV yourself, or type
  it by hand.
- **No GUI.** Command line only, so it runs anywhere Python runs, including JupyterHub.
- **No storage.** Nothing is written to disk and nothing is uploaded. The file is read, the number is printed,
  the process exits.

## Development

```bash
git clone https://github.com/chenhn2026-dot/cityugpa
cd cityugpa
python3 -m pip install -e .
python3 -m pytest -q
```

`pip install -e .` installs the folder you are standing in, in editable mode: change the source, and the next
command you run uses the new code.

## License

MIT. See [LICENSE](LICENSE).
