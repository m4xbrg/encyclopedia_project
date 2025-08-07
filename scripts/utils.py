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
    "|": r"\textbar{}",
    "<": r"\textless{}",
    ">": r"\textgreater{}",
=======
    "\\": r"\\textbackslash{}",
    "#": r"\#", "$": r"\$", "%": r"\%", "&": r"\&",
    "~": r"\textasciitilde{}", "_": r"\_", "^": r"\^{}",
    "{": r"\{", "}": r"\}",
}

SPECIAL_LATEX_RE = re.compile(
    "|".join(re.escape(char) for char in SPECIAL_LATEX_CHARS)
)


def escape_latex(text: str) -> str:
    """Escape LaTeX special characters in ``text``.

    Each character listed in ``SPECIAL_LATEX_CHARS`` is replaced in a single
    regular-expression pass to avoid double-escaping replacements that include
    other special characters.
    """

    return SPECIAL_LATEX_RE.sub(lambda m: SPECIAL_LATEX_CHARS[m.group()], text)


def normalize_artifacts(text: str) -> str:
    return (
        text.replace("“", '"').replace("”", '"')
            .replace("‘", "'").replace("’", "'")
            .replace("--", "---").replace("...", r"\ldots{}")
    )

# --- Prompt & Filename Helpers ---
def render_prompt(template_str: str, **kwargs: Any) -> str:
    return Template(template_str).safe_substitute(**kwargs)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "entry"


def sanitize_filename(text: str) -> str:
    return f"{slugify(text)}.tex"
