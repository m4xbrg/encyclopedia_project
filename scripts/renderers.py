"""Renderer abstractions for generating different output formats."""

from __future__ import annotations

from abc import ABC, abstractmethod
import re
from html import escape as html_escape

from utils import normalize_artifacts, escape_latex


class Renderer(ABC):
    """Abstract base class for output renderers."""

    #: File extension used for rendered output
    extension: str = "txt"

    @abstractmethod
    def convert(self, text: str) -> str:
        """Convert raw markdown text into renderer specific markup."""

    @abstractmethod
    def wrap(
        self, *, title: str, id: str, domain: str, topic: str, body: str
    ) -> str:
        """Wrap the converted body with any document boilerplate."""


class LatexRenderer(Renderer):
    """Renderer implementing the current LaTeX output behaviour."""

    extension = "tex"

    MD_PATTERNS = [
        (re.compile(r"`([^`]+)`"), r"\\texttt{\1}"),
        (re.compile(r"\*\*(.+?)\*\*", re.DOTALL), r"\\textbf{\1}"),
        (
            re.compile(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", re.DOTALL),
            r"\\textit{\1}",
        ),
    ]

    TEX_WRAPPER = r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb}
\usepackage{geometry}
\usepackage{titlesec}
\usepackage{hyperref}
\geometry{margin=1in}

\titleformat{\section}[block]{\large\bfseries}{}{0em}{}
\titleformat{\subsection}[block]{\normalsize\bfseries}{}{0em}{}

\begin{document}

% Title: {title}
% ID: {id}
% Domain: {domain}
% Topic: {topic}

{body}

\end{document}
"""

    def _replace_md(self, seg: str) -> str:
        for pat, repl in self.MD_PATTERNS:
            seg = pat.sub(repl, seg)
        return seg

    def convert(self, text: str) -> str:
        """Convert basic Markdown to LaTeX, preserve math, then escape."""
        math_pat = re.compile(r"\\\$.*?\\\$|\\\\\[.*?\\\\\]", re.DOTALL)
        parts, last = [], 0
        for m in math_pat.finditer(text):
            raw = text[last : m.start()]
            raw = self._replace_md(raw)
            raw = normalize_artifacts(raw)
            raw = escape_latex(raw)
            parts.append(raw)
            parts.append(m.group())
            last = m.end()
        tail = text[last:]
        tail = self._replace_md(tail)
        tail = normalize_artifacts(tail)
        tail = escape_latex(tail)
        parts.append(tail)
        return "".join(parts)

    def wrap(
        self, *, title: str, id: str, domain: str, topic: str, body: str
    ) -> str:
        return self.TEX_WRAPPER.format(
            title=title, id=id, domain=domain, topic=topic, body=body
        )


class HtmlRenderer(Renderer):
    """Placeholder HTML renderer to demonstrate extensibility."""

    extension = "html"

    def convert(self, text: str) -> str:  # pragma: no cover - placeholder
        return text

    def wrap(
        self, *, title: str, id: str, domain: str, topic: str, body: str
    ) -> str:
        return (
            "<!DOCTYPE html>\n"
            "<html><head><meta charset=\"utf-8\">"
            f"<title>{html_escape(title)}</title></head><body>\n"
            f"<!-- ID: {html_escape(id)} -->\n"
            f"<!-- Domain: {html_escape(domain)} -->\n"
            f"<!-- Topic: {html_escape(topic)} -->\n"
            f"{body}\n"
            "</body></html>"
        )

