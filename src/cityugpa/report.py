# src/cityugpa/report.py
import time
import sys

CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

def pad(text, width):
    text = str(text)
    w = sum(2 if ord(c) > 0x2E80 else 1 for c in text)
    return text + " " * max(0, width - w)

def animate_loading():
    chars = "|/-\\"
    sys.stdout.write(f"{CYAN}⏳ Calculating GPA... {RESET}")
    for _ in range(10):
        for char in chars:
            sys.stdout.write(f"\r{CYAN}⏳ Calculating GPA... {char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.02)
    sys.stdout.write("\r" + " " * 40 + "\r")

def print_term_report(records, result):
    animate_loading()
    print(f"\n{BOLD}{YELLOW}Semester A 2026-27{RESET}")
    
    print(f"{CYAN}┏━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓{RESET}")
    print(f"{CYAN}┃{RESET} {BOLD}{pad('Code', 10)}{RESET} {CYAN}┃{RESET} {BOLD}{pad('Units', 6)}{RESET} {CYAN}┃{RESET} {BOLD}{pad('Grade', 6)}{RESET} {CYAN}┃{RESET} {BOLD}{pad('Point', 6)}{RESET} {CYAN}┃{RESET}")
    print(f"{CYAN}┣━━━━━━━━━━━━╋━━━━━━━━╋━━━━━━━━╋━━━━━━━━┫{RESET}")
    
    mock_points = {"A-": 3.7, "B+": 3.3, "B": 3.0, "A": 4.0, "A+": 4.3, "F": 0.0}
    
    for r in records:
        point = mock_points.get(r.grade.strip(), "--")
        point_str = f"{point:.1f}" if isinstance(point, float) else point
        point_color = RED if point == 0.0 else GREEN
        print(f"{CYAN}┃{RESET} {pad(r.code, 10)} {CYAN}┃{RESET} {pad(str(int(r.units))+' CU', 6)} {CYAN}┃{RESET} {pad(r.grade, 6)} {CYAN}┃{RESET} {point_color}{pad(point_str, 6)}{RESET} {CYAN}┃{RESET}")
        
    print(f"{CYAN}┗━━━━━━━━━━━━┻━━━━━━━━┻━━━━━━━━┻━━━━━━━━┛{RESET}")
    
    sgpa_str = f"{result.sgpa:.2f}" if result.sgpa is not None else "N/A"
    cgpa_str = f"{result.cgpa:.2f}" if result.cgpa is not None else "N/A"
    
    print(f"\n{BOLD}SGPA:{RESET} {GREEN if result.sgpa and result.sgpa >= 3.0 else RED}{sgpa_str}{RESET}  ({result.gpa_units:.0f} CU in GPA, {result.earned_units:.0f} CU earned)")
    print(f"{BOLD}CGPA:{RESET} {cgpa_str}  ({result.earned_units:.0f} CU)\n")


# 注意看，这里是一个独立的函数！它被放在了外面！
def print_deans_list(result):
    sgpa_str = f"{result.sgpa:.2f}" if result.sgpa is not None else "N/A"
    is_deans = result.sgpa is not None and result.sgpa >= 3.7 and result.gpa_units >= 12
    
    if is_deans:
        print(f"{GREEN}{BOLD}          ___________________________")
        print(f"         /                           \\")
        print(f"        |     🎓  DEAN'S LIST  🎓     |")
        print(f"        |       CONGRATULATIONS       |")
        print(f"        |       SGPA: {sgpa_str} (>=3.70)     |")
        print(f"         \\___________________________/")
        print(f"                    \\   ^__^")
        print(f"                     \\  (oo)\\_______")
        print(f"                        (__)\\       )\\/\\")
        print(f"                            ||----w |")
        print(f"                            ||     ||{RESET}\n")
    else:
        print(f"{RED}Dean's List: Not Qualified (SGPA {sgpa_str} < 3.70 or insufficient credits){RESET}\n")


def print_target(required_point, possible):
    print(f"{BOLD}🎯 Target Plan:{RESET}")
    if possible:
        print(f"   You need an average GPA of {GREEN}{required_point:.2f}{RESET} in remaining courses.\n")
    else:
        print(f"   {RED}❌ Target is impossible. Required GPA {required_point:.2f} exceeds maximum limit.{RESET}\n")