"""Grade scale loading and the CityU grade -> grade point mapping."""

import json
from importlib.resources import files

def load_scale(scale_name: str = "cityu"):
    resource = files("cityugpa.scales").joinpath(f"{scale_name}.json")
    with resource.open("r", encoding="utf-8") as f:
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
            return (points_dict[base_grade], False)
        raise ValueError(f"未知成绩: {grade}")

    # 不带星
    if grade in points_dict:
        return (points_dict[grade], grade not in excluded)
    if grade in excluded:
        return (None, False)
    raise ValueError(f"未知成绩: {grade}")


def can_earn_credit(grade, scale):
    """这个成绩能不能算进毕业学分。

    带星成绩的学分不计入毕业最低学分要求，Z 也不给学分；
    P / TR 照拿学分，只是不进 GPA。
    """
    grade = grade.strip()
    if grade.endswith("*"):
        return False
    return grade in scale["earns_credit"]
