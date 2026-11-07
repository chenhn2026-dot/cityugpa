# src/cityugpa/report.py

def print_mock_report(filename=""):
    if filename:
        print(f"trying to read the file: {filename} ('data will update later')\n")

    print("Semester A 2026-27")
    print("COMP1021  3 CU  A-  3.7")
    print("MATH1011  3 CU  B+  3.3")
    print("GE1401    3 CU  B   3.0")
    print("LANG1001  3 CU  P   --")
    print("")
    print("SGPA: 3.41 (12 CU in GPA, 12 CU earned)")
    print("CGPA: 3.28 (54 CU)")
    print("Dean's List: Fail (SGPA 3.41 < 3.70)")