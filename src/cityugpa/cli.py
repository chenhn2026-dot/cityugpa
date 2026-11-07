# src/cityugpa/cli.py
import argparse
from cityugpa.report import print_mock_report

def main():
    parser = argparse.ArgumentParser(
        prog="cityugpa", 
        description="Calculate CityU GPA under official academic rules"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    #add term instru
    parser_term = subparsers.add_parser("term", help="Calculate semester SGPA")
    parser_term.add_argument("file", type=str, help="Path to CSV file")

    #add cgpa instru
    parser_cgpa = subparsers.add_parser("cgpa", help="Calculate cumulative CGPA")
    parser_cgpa.add_argument("file", type=str, help="Path to CSV file")

    args = parser.parse_args()

    if args.command in ["term", "cgpa"]:
        print_mock_report(args.file)

if __name__ == "__main__":
    main()