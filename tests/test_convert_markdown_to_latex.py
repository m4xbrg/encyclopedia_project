from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from generate import convert_markdown_to_latex


def test_inline_math_preserved():
    src = "Euler's identity $e^{i\\pi}+1=0$ is neat."
    assert convert_markdown_to_latex(src) == src


def test_multiline_math_preserved():
    src = "A theorem:\n\\[a^2 + b^2 = c^2\\]"
    assert convert_markdown_to_latex(src) == src


def test_literal_dollar_escaped():
    src = "Price is $5."
    assert convert_markdown_to_latex(src) == "Price is \\$5."

