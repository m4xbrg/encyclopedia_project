from __future__ import annotations

import re
from pathlib import Path
from string import Template
from typing import Any

# --- Sanitization Helpers ---
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
}


def escape_latex(text: str) -> str:
    for char, repl in SPECIAL_LATEX_CHARS.items():
        text = text.replace(char, repl)
    return text


def normalize_artifacts(text: str) -> str:
    return (
        text.replace("“", '"')
            .replace("”", '"')
            .replace("‘", "'")
            .replace("’", "'")
            .replace("--", "---")
            .replace("...", r"\ldots{}")
    )


# --- Prompt & Filename Helpers ---
def render_prompt(template_str: str, **kwargs: Any) -> str:
    return Template(template_str).safe_substitute(**kwargs)


# Slug rules
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
MAX_SLUG_LENGTH = 64


def slugify(text: str) -> str:
    """Convert *text* to a filesystem-friendly slug.

    The slug must consist of lowercase ASCII letters, numbers and dashes, and
    may not exceed ``MAX_SLUG_LENGTH`` characters.  A ``ValueError`` is raised if
    the resulting slug violates these rules.
    """

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
    """Slugify *text* and ensure the resulting filename is unique."""

    directory = directory or Path(".")
    slug = slugify(text)
    path = directory / f"{slug}.tex"
    return dedupe_path(path)

