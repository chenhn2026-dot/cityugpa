import pytest
from cityugpa.scale import load_scale, grade_point, can_earn_credit

s = load_scale("cityu")

def test_normal_grade():
    assert grade_point("A-", s) == (3.7, True)

def test_star_grade():
    # A+* 自动识别，不需要在json里写A+*
    assert grade_point("A+*", s) == (4.3, False)

def test_p():
    assert grade_point("P", s) == (None, False)

def test_tr():
    assert grade_point("TR", s) == (None, False)

def test_z():
    assert grade_point("Z", s) == (None, False)

def test_unknown_raise():
    with pytest.raises(ValueError) as exc_info:
        grade_point("X9", s)
    assert "X9" in str(exc_info.value)

def test_strip_space():
    assert grade_point(" A+* ", s) == (4.3, False)

def test_credit_for_p_and_tr():
    # P 和 TR 拿学分，只是不算 GPA
    assert can_earn_credit("P", s) is True
    assert can_earn_credit("TR", s) is True

def test_no_credit_for_star_and_z():
    # 带星的学分不计入毕业要求，Z 什么都不给
    assert can_earn_credit("A+*", s) is False
    assert can_earn_credit("Z", s) is False
