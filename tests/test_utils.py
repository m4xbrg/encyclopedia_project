import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from utils import slugify, dedupe_path


def test_slugify_rejects_too_long():
    text = "a" * 65
    with pytest.raises(ValueError):
        slugify(text)


def test_slugify_rejects_empty():
    with pytest.raises(ValueError):
        slugify("!!!")


def test_dedupe_path_appends_suffix(tmp_path: Path):
    first = tmp_path / "entry.tex"
    first.touch()

    next_path = dedupe_path(first)
    assert next_path.name == "entry-2.tex"

    next_path.touch()
    third = dedupe_path(first)
    assert third.name == "entry-3.tex"

