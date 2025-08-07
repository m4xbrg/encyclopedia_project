from __future__ import annotations

import re
from pathlib import Path
from string import Template
from typing import Any

SPECIAL_LATEX_CHARS = {
    "#": r"\#",
    "$": r"\$",
    "%": r"\%",
    "&": r"\&",
    "~": r"\textasciitilde{}",
    "_": r"\_",
    "^": r"\^{}",
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "|": r"\textbar{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
}

SPECIAL_LATEX_RE = re.compile("|".join(re.escape(c) for c in SPECIAL_LATEX_CHARS))

def escape_latex(text: str) -> str:
    """Escape LaTeX special characters in ``text``."""
    return SPECIAL_LATEX_RE.sub(lambda m: SPECIAL_LATEX_CHARS[m.group()], text)

def normalize_artifacts(text: str) -> str:
    """Normalise common Unicode punctuation and ellipsis/dash artifacts."""
    text = (
        text.replace("“", '"')
            .replace("”", '"')
            .replace("‘", "'")
            .replace("’", "'")
    )
    text = re.sub(r"(?<!-)--(?!-)", "---", text)
    text = re.sub(r"(?<!\.)\.{3}(?!\.)", r"\\ldots{}", text)
    return text

def render_prompt(template_str: str, **kwargs: Any) -> str:
    """Substitute variables in a template string."""
    return Template(template_str).safe_substitute(**kwargs)

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
MAX_SLUG_LENGTH = 64

def slugify(text: str) -> str:
    """Convert *text* to a filesystem-safe slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    slug = text.strip("-")
    if not slug:
        raise ValueError("slug has no valid characters")
    if len(slug) > MAX_SLUG_LENGTH:
        raise ValueError(f"slug exceeds {MAX_SLUG_LENGTH} characters")
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("slug contains invalid characters")
    return slug

def dedupe_path(path: Path) -> Path:
    """Return a unique path, appending ``-N`` if needed."""
    base = path.stem
    suffix = path.suffix
    candidate = path
    n = 1
    while candidate.exists():
        n += 1
        candidate = path.with_name(f"{base}-{n}{suffix}")
    return candidate

def sanitize_filename(text: str, directory: Path | None = None) -> Path:
    """Slugify *text* and ensure filename is unique within *directory*."""
    directory = directory or Path(".")
    slug = slugify(text)
    path = directory / f"{slug}.tex"
    return dedupe_path(path)
