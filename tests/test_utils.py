import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
from utils import normalize_artifacts


def test_basic_replacements():
    text = "Wait -- what..."
    expected = "Wait --- what\\ldots{}"
    assert normalize_artifacts(text) == expected


def test_preserves_existing_artifacts():
    text = "An em --- dash and an ellipsis \\ldots{} stay."
    assert normalize_artifacts(text) == text


def test_normalize_artifacts_idempotent():
    text = "We have -- and ... plus --- and \\ldots{}"
    once = normalize_artifacts(text)
    twice = normalize_artifacts(once)
    assert once == twice
    assert once == "We have --- and \\ldots{} plus --- and \\ldots{}"
