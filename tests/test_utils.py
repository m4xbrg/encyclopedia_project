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

=======
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
