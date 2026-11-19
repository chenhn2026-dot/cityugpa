# src/cityugpa/report.py
import time
import sys
import shutil

# ANSI color codes
CYAN = "\033[96m"
MAGENTA = "\033[95m" # 新增粉色，用于撞色
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"
BG_DARK = "\033[48;5;236m"

# 🌟 极客风立体 LOGO（青色与粉色撞色）
LOGO = rf"""{CYAN}{BOLD}
    ██████╗██╗████████╗██╗   ██╗██╗   ██╗     ██████╗ ██████╗  █████╗ 
   ██╔════╝██║╚══██╔══╝╚██╗ ██╔╝██║   ██║    ██╔════╝ ██╔══██╗██╔══██╗
   ██║     ██║   ██║    ╚████╔╝ ██║   ██║    ██║  ███╗██████╔╝███████║
   ██║     ██║   ██║     ╚██╔╝  ██║   ██║    ██║   ██║██╔═══╝ ██╔══██║
   ╚██████╗██║   ██║      ██║   ╚██████╔╝    ╚██████╔╝██║     ██║  ██║
    ╚═════╝╚═╝   ╚═╝      ╚═╝    ╚═════╝      ╚═════╝ ╚═╝     ╚═╝  ╚═╝{MAGENTA}
{RESET}"""

def pad(text, width):
    """Pad text based on display width (CJK chars count as 2)."""
    text = str(text)
    w = sum(2 if ord(c) > 0x2E80 else 1 for c in text)
    return text + " " * max(0, width - w)

def show_progress_bar():
    """带渐变色的极客进度条"""
    total = 30
    for i in range(total + 1):
        percent = int(100 * i / total)
        # 前 15 格青色，后 15 格粉色
        bar = (f"{CYAN}█" * min(i, 15)) + (f"{MAGENTA}█" * max(0, i - 15)) + (f"{RESET}░" * (total - i))
        sys.stdout.write(f"\r{BOLD}Analyzing Data:{RESET} |{bar}{RESET}| {percent:3d}%")
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n")

def print_term_report(records, result):
    # 1. 打印超帅 Logo
    print(LOGO)
    
    # 2. 获取终端宽度，画分割线
    terminal_width = shutil.get_terminal_size().columns
    print(f"{CYAN}" + "━" * min(terminal_width, 70) + f"{RESET}")
    
    # 3. 播放进度条
    show_progress_bar()
    
    print(f"{BOLD}{YELLOW}Semester A 2026-27{RESET}")
    
    # 表格头
    print(f"{CYAN}┏━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓{RESET}")
    print(f"{CYAN}┃{RESET} {BOLD}{pad('Code', 10)}{RESET} {CYAN}┃{RESET} {BOLD}{pad('Units', 6)}{RESET} {CYAN}┃{RESET} {BOLD}{pad('Grade', 6)}{RESET} {CYAN}┃{RESET} {BOLD}{pad('Point', 6)}{RESET} {CYAN}┃{RESET}")
    print(f"{CYAN}┣━━━━━━━━━━━━╋━━━━━━━━╋━━━━━━━━╋━━━━━━━━┫{RESET}")
    
    mock_points = {"A-": 3.7, "B+": 3.3, "B": 3.0, "A": 4.0, "A+": 4.3, "F": 0.0}
    
    for i, r in enumerate(records):
        point = mock_points.get(r.grade.strip(), "--")
        point_str = f"{point:.1f}" if isinstance(point, float) else point
        point_color = RED if point == 0.0 else GREEN
        
        # 4. 斑马线背景
        bg = BG_DARK if i % 2 == 0 else ""
        
        row_str = f"{CYAN}┃{RESET}{bg} {pad(r.code, 10)} {CYAN}┃{RESET}{bg} {pad(str(int(r.units))+' CU', 6)} {CYAN}┃{RESET}{bg} {pad(r.grade, 6)} {CYAN}┃{RESET}{bg} {point_color}{pad(point_str, 6)}{RESET}{bg} {CYAN}┃{RESET}"
        print(row_str)
        
    print(f"{CYAN}┗━━━━━━━━━━━━┻━━━━━━━━┻━━━━━━━━┻━━━━━━━━┛{RESET}")
    
    sgpa_str = f"{result.sgpa:.2f}" if result.sgpa is not None else "N/A"
    cgpa_str = f"{result.cgpa:.2f}" if result.cgpa is not None else "N/A"
    
    print(f"\n{BOLD}SGPA:{RESET} {GREEN if result.sgpa and result.sgpa >= 3.0 else RED}{sgpa_str}{RESET}  ({result.gpa_units:.0f} CU in GPA, {result.earned_units:.0f} CU earned)")
    print(f"{BOLD}CGPA:{RESET} {cgpa_str}  ({result.earned_units:.0f} CU)\n")

def print_deans_list(result):
    sgpa_str = f"{result.sgpa:.2f}" if result.sgpa is not None else "N/A"
    is_deans = result.sgpa is not None and result.sgpa >= 3.7 and result.gpa_units >= 12
    
    if is_deans:
        # 5. 豪华学术风奖状 + 保留小奶牛
        print(f"{GREEN}{BOLD}")
        print(f"    ✦ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ✦")
        print(f"    ┃                               ┃")
        print(f"    ┃        ★  DEAN'S LIST  ★      ┃")
        print(f"    ┃         CONGRATULATIONS       ┃")
        print(f"    ┃        SGPA: {sgpa_str} (>=3.70)    ┃")
        print(f"    ┃                               ┃")
        print(f"    ┃          \\   ^__^             ┃")
        print(f"    ┃           \\  (oo)\\_______     ┃")
        print(f"    ┃              (__)\\       )\\/\\ ┃")
        print(f"    ┃                   ||----w |   ┃")
        print(f"    ┃                   ||     ||   ┃")
        print(f"    ✦ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ✦")
        print(f"{RESET}\n")
    else:
        print(f"{RED}Dean's List: Not Qualified (SGPA {sgpa_str} < 3.70 or insufficient credits){RESET}\n")

def print_target(required_point, possible):
    print(f"{BOLD}🎯 Target Plan:{RESET}")
    if possible:
        print(f"   You need an average GPA of {GREEN}{required_point:.2f}{RESET} in remaining courses.\n")
    else:
        print(f"   {RED}❌ Target is impossible. Required GPA {required_point:.2f} exceeds maximum limit.{RESET}\n")