import json

def load_scale(path=None):
    """读JSON，返回一个dict。path为空时用内置的scales/cityu.json。"""
    if path is None:
        path = "scales/cityu.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def grade_point(grade, scale):
    """
    把成绩翻译成 (绩点, 是否计入GPA)
    带*后缀：有绩点，但不计入GPA
    """
    grade = grade.strip()
    points_dict = scale["points"]
    excluded = scale["excluded_from_gpa"]

    # 规则：末尾带*，单独处理
    if grade.endswith("*"):
        base_grade = grade[:-1]
        if base_grade in points_dict:
            gpa_val = points_dict[base_grade]
            return (gpa_val, False)
        else:
            raise ValueError(f"未知成绩: {grade}")

    # 不带星，原有逻辑
    if grade in points_dict:
        gpa_val = points_dict[grade]
        count_in_gpa = grade not in excluded
        return (gpa_val, count_in_gpa)
    elif grade in excluded:
        return (None, False)
    else:
        raise ValueError(f"未知成绩: {grade}")
