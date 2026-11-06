\# cityugpa



Calculate your GPA the way City University of Hong Kong actually does.



\## Why this exists



CityU truncates the GPA to two decimal places instead of rounding it, counts

failed courses in the GPA, and includes only the latest attempt in the CGPA

when a course is repeated. Most online GPA calculators get all three wrong.



\## Install



&#x20;   pip install cityugpa



\## Usage



&#x20;   cityugpa term examples/fake\_transcript.csv

&#x20;   cityugpa cgpa examples/fake\_transcript.csv

&#x20;   cityugpa deans-list examples/fake\_transcript.csv

&#x20;   cityugpa target --goal 3.6 --remaining 15 examples/fake\_transcript.csv



\## Rules implemented



| Rule | Source |

|---|---|

| GPA truncated to 2 decimals, not rounded | ARRO Course Grades |

| Failed courses counted | ARRO Course Grades |

| Repeated course: latest attempt only | ARRO Course Grades |

| Asterisked grades excluded | ARRO Course Grades |



\## What this does not do



\- It does not connect to AIMS.

\- It does not store any grade data.

\- It has no GUI.



\## Development



&#x20;   git clone https://github.com/chenhn2026-dot/cityugpa.git

&#x20;   pip install -e .

&#x20;   pytest

