import pytest
from scale import load_scale, grade_point

s = load_scale()

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
