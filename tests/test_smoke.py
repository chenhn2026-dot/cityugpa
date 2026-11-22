import re
import cityugpa


def test_version_exists():
    assert cityugpa.__version__


def test_version_is_a_release_number():
    assert re.fullmatch(r"\d+\.\d+\.\d+", cityugpa.__version__), cityugpa.__version__
