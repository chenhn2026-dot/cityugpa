# cityugpa

Calculate your GPA the way City University of Hong Kong actually does.

## Why this exists

CityU truncates the GPA to two decimal places instead of rounding it. It also
counts failed courses in the GPA, and includes only the latest attempt in the
CGPA when a course is repeated. Most online GPA calculators get all three wrong.

## Install

    pip install cityugpa

## Usage

    cityugpa term examples/fake_transcript.csv
    cityugpa cgpa examples/fake_transcript.csv
    cityugpa deans-list examples/fake_transcript.csv
    cityugpa target --goal 3.6 --remaining 15 examples/fake_transcript.csv

## Rules implemented

- GPA truncated to two decimals, not rounded
- Failed courses counted in the GPA
- Repeated courses: only the latest attempt counts in the CGPA
- Asterisked grades excluded from the GPA

## What this does not do

- It does not connect to AIMS.
- It does not store any grade data.
- It has no GUI.

## Development

    git clone https://github.com/chenhn2026-dot/cityugpa.git
    cd cityugpa
    pip install -e .
    pytest
