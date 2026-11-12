# src/cityugpa/cli.py
# src/cityugpa/cli.py
import argparse
import sys
from cityugpa.parser import parse_csv
from cityugpa.calc import compute, plan_target
from cityugpa.scale import load_scale
from cityugpa.report import print_term_report, print_deans_list, print_target


def main():
    parser = argparse.ArgumentParser(prog="cityugpa", description="Calculate CityU GPA")
    sub = parser.add_subparsers(dest="command", required=True)

    # 1. term
    p = sub.add_parser("term", help="算一个学期 SGPA")
    p.add_argument("file", type=str)

    # 2. cgpa
    p = sub.add_parser("cgpa", help="算累计 CGPA")
    p.add_argument("file", type=str)

    # 3. deans-list
    p = sub.add_parser("deans-list", help="判断 Dean's List")
    p.add_argument("file", type=str)

    # 4. target（反推目标分）
    p = sub.add_parser("target", help="反推目标 GPA 还需多少分")
    p.add_argument("--goal", type=float, required=True)
    p.add_argument("--remaining", type=int, required=True, help="剩余学分")
    p.add_argument("file", type=str)

    args = parser.parse_args()

    # 退出码1：文件/数据问题
    try:
        scale = load_scale()
        records = parse_csv(args.file)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # 计算
    try:
        result = compute(records, scale)
    except Exception as e:
        print(f"Calculation error: {e}", file=sys.stderr)
        sys.exit(1)

    # 分发输出
    if args.command == "term":
        print_term_report(records, result)
    elif args.command == "cgpa":
        print(f"CGPA: {result.cgpa:.2f} ({result.gpa_units:.0f} CU)") if result.cgpa is not None else print("CGPA: N/A")
    elif args.command == "deans-list":
        print_deans_list(result)
    elif args.command == "target":
        required, possible = plan_target(result.cgpa, result.gpa_units, args.goal, args.remaining)
        print_target(required, possible)

    sys.exit(0)  # 正常退出码


if __name__ == "__main__":
    main()