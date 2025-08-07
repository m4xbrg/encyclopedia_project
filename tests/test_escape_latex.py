import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from utils import escape_latex, SPECIAL_LATEX_CHARS


@pytest.mark.parametrize("char,expected", SPECIAL_LATEX_CHARS.items())
def test_escape_individual_chars(char, expected):
    assert escape_latex(char) == expected


def test_escape_combined_chars():
    text = "".join(SPECIAL_LATEX_CHARS.keys())
    expected = "".join(SPECIAL_LATEX_CHARS[c] for c in SPECIAL_LATEX_CHARS)
    assert escape_latex(text) == expected


def test_escape_without_special_chars():
    text = "Hello World!"
    assert escape_latex(text) == text
