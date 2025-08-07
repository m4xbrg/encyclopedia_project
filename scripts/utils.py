"""Utility helpers for the super_encyclopedia_rebuild project."""
from __future__ import annotations

import re
from pathlib import Path
from string import Template
from typing import Any


def render_prompt(template_str: str, **kwargs: Any) -> str:
    """Render a template string using keyword arguments."""
    return Template(template_str).safe_substitute(**kwargs)


def slugify(text: str) -> str:
    """Convert text into a filesystem-friendly slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "entry"


def sanitize_filename(text: str) -> str:
    """Return a sanitized filename for the given text with a .tex extension."""
    return f"{slugify(text)}.tex"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")

