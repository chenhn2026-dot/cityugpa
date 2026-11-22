# cityugpa

Calculate your CityU GPA strictly by [CityU ARRO official rules](https://www.cityu.edu.hk/arro/asmt/cgrd_main.htm) — right from your terminal, with zero dependencies and zero data uploaded.

[![PyPI](https://img.shields.io/badge/pypi-cityugpa-blue)](https://pypi.org/project/cityugpa/)
[![CI](https://github.com/chenhn2026-dot/cityugpa/actions/workflows/ci.yml/badge.svg)](https://github.com/chenhn2026-dot/cityugpa/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Privacy first:** Everything runs locally in memory. `cityugpa` does not log into AIMS, does not store your grades, and never uploads any data.

---

## Why `cityugpa`?

Most online GPA calculators give a different number from your CityU transcript because CityU applies five specific rules:

| Rule | CityU Official Rule | Generic Calculators |
| --- | --- | --- |
| **Truncate, never round** | `41.0 ÷ 12 = 3.4166…` → **`3.41`** | Rounds to `3.42` |
| **Failed courses (`F`)** | Counted as `0.0` in GPA | Often skipped |
| **Retakes** | Only the **latest** attempt counts in CGPA | Counts both attempts |
| **Starred grades (`A+*`)** | Excluded from both GPA and earned credits | Counted as `A+` |
| **Non-graded marks** | `P`/`TR` earn credit (no points); `Z`/`IP`/`I`/`X`/`WD`/`AU` earn neither | Miscounted as `0.0` |

---

## Use Cases

- **Check a number you do not trust.** AIMS says `3.41` but the online calculator said `3.42` — paste your grades and see which rule the calculator ignored.
- **Plan the next semester.** `cityugpa target --goal 3.6 --remaining 15 my_grades.csv` answers "what average do I need from here" before course selection closes.
- **Understand a retake.** See exactly what a repeat course does to CGPA, and whether the first attempt still counts.
- **Check the Dean's List line early.** It is a credit threshold *and* a GPA threshold — one command tells you how far you are from both.

---

## Quick Start (Beginner-Friendly, 3 Minutes)

Never used a terminal before? Just follow these three steps in order.

### Step 1. Open your terminal & check Python

- **macOS:** Press `Command` + `Space`, type `Terminal`, press Enter.
- **Windows:** Press the Windows key, type `PowerShell`, press Enter.

Type this command and press Enter:

```bash
python3 --version
```

You should see something like `Python 3.12.4`. Any version **3.10 or newer** works.

- If `python3` is not found on Windows, try `python --version`.
- If Python is missing or older than 3.10, install it from [python.org/downloads](https://www.python.org/downloads/) (on Windows, tick **"Add python.exe to PATH"** on the first installer screen).

### Step 2. Install `cityugpa`

```bash
pip install cityugpa
```

If `pip` is not recognized, run:

```bash
python3 -m pip install cityugpa
```

> **Installing from a downloaded folder instead?** Run `pip install .` inside the project folder.

Verify the installation:

```bash
cityugpa --help
```

You should see the four subcommands: `term`, `cgpa`, `deans-list`, and `target`. (If `cityugpa` is not on your `PATH`, use `python3 -m cityugpa.cli --help`.)

### Step 3. Create your CSV & calculate your GPA

Create a plain-text file named `my_grades.csv` with four columns (`code,units,grade,term`):

```csv
code,units,grade,term
MA1508,4,A-,2026A
MA1503,4,B+,2026A
CS1302A,3,B,2026A
CS2613,1,A,2026A
GE1401,3,P,2026A
GE2313,3,A+*,2026A
GE2410,3,Z,2026A
```

> **Tip:** In Excel, use **File → Save As → CSV UTF-8 (Comma delimited)**.

Run:

```bash
cityugpa term my_grades.csv
```

Output:

```
Semester A 2026-27
MA1508       4 CU   A-      3.70
MA1503       4 CU   B+      3.30
CS1302A      3 CU   B       3.00
CS2613       1 CU   A       4.00
GE1401       3 CU   P         --
GE2313       3 CU   A+*       --
GE2410       3 CU   Z         --

SGPA: 3.41   (12 CU in GPA, 15 CU earned)
CGPA: 3.41   (12 CU)
```

Notice why it is **3.41** (not 3.42): `(4×3.70 + 4×3.30 + 3×3.00 + 1×4.00) / 12 = 41.0 / 12 = 3.4166…`, truncated to two decimal places.

---

## Commands

| Command | What it does | Example |
| --- | --- | --- |
| `term <file>` | Semester GPA (SGPA), earned credits, and line-by-line breakdown | `cityugpa term my_grades.csv` |
| `cgpa <file>` | Cumulative GPA across all terms (latest attempt only for retakes) | `cityugpa cgpa my_retakes.csv` |
| `deans-list <file>` | Checks Dean's List eligibility (`>= 12 CU`, `SGPA >= 3.70`, no `F`) | `cityugpa deans-list my_grades.csv` |
| `target --goal <G> --remaining <CU> <file>` | Calculates the average GPA needed over your remaining credits | `cityugpa target --goal 3.6 --remaining 15 my_grades.csv` |

### Retake & Failed Course Example (`cgpa`)

```csv
code,units,grade,term
CS2310,3,C+,2025A
CS2310,3,B+,2026A
CS2613,1,F,2026A
MA2185,3,A-,2026A
```

```bash
cityugpa cgpa my_retakes.csv
```

- `CS2310` keeps only the latest `2026A` attempt (`B+`, `3.30`), dropping `2025A` (`C+`).
- `CS2613` (`F`) stays in the GPA with `0.00` points.
- Result: **`CGPA: 3.00 (7 CU)`**.

### Target GPA Example (`target`)

```bash
cityugpa target --goal 3.6 --remaining 15 my_grades.csv
```

```
Current: 3.41 over 12 CU
Goal:    3.60 over 27 CU
Needed:  3.75 average over the next 15 CU (possible)
```

### Exit Codes

- `0`: Success
- `1`: File not found or invalid CSV content (reports the exact line number)
- `2`: Invalid CLI arguments

---

## CSV Format Rules

- **Required header:** `code,units,grade,term`
- **Case-insensitive grades:** `a-` is normalized to `A-`.
- **Excel UTF-8 BOM & blank lines:** Handled automatically.
- **Strict validation:** Missing values, unknown grades (e.g. `B++`), or non-numeric `units` stop immediately with a line-number error.

---

## Troubleshooting

| Error | Fix |
| --- | --- |
| `command not found: python3` | Install Python 3.10+ from [python.org/downloads](https://www.python.org/downloads/) |
| `command not found: pip` | Use `python3 -m pip install cityugpa` |
| `command not found: cityugpa` | Run `python3 -m cityugpa.cli --help` |
| `error: externally-managed-environment` | Use a virtual environment (`python3 -m venv .venv`) or `pip install --user cityugpa` |

---

## How It Works

```
CSV file → parser.py → scale.py → calc.py → report.py → Terminal
```

- `parser.py`: Reads and validates CSV rows with line-number error reporting.
- `scale.py`: Maps CityU letter grades and non-graded marks to `(grade_point, counts_in_gpa, earns_credit)`.
- `calc.py`: Deduplicates retakes by latest term and truncates GPA using `math.floor(x * 100 + 1e-9) / 100`.
- `report.py`: Formats aligned terminal tables and summaries.

---

## Development

```bash
git clone https://github.com/chenhn2026-dot/cityugpa.git
cd cityugpa
python3 -m pip install -e .
python3 -m pytest -q
```

---

## License

MIT — see [LICENSE](LICENSE).

## CLI Usage
- `cityugpa term <file.csv>`: Calculate semester SGPA
- `cityugpa cgpa <file.csv>`: Calculate cumulative CGPA
- `cityugpa deans-list <file.csv>`: Check Dean's List qualification
- `cityugpa target --goal <gpa> --remaining <units> <file.csv>`: Reverse calculate target GPA
