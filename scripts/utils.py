from __future__ import annotations
import re
from pathlib import Path
from string import Template
from typing import Any

# --- Sanitization Helpers ---
SPECIAL_LATEX_CHARS = {
    "#": r"\#", "$": r"\$", "%": r"\%", "&": r"\&",
    "~": r"\textasciitilde{}", "_": r"\_", "^": r"\^{}",
    "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}" ,
}

def escape_latex(text: str) -> str:
    for char, repl in SPECIAL_LATEX_CHARS.items():
        text = text.replace(char, repl)
    return text


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