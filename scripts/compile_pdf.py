"""Compile Markdown files in the output directory into PDFs.

This script performs light validation and preprocessing before invoking
`pandoc` to convert Markdown files into PDFs.  Results are written to the
`pdf_output` directory and a log of successes and failures is appended to
`logs/compile_log.txt`.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Tuple


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"
PDF_OUTPUT_DIR = ROOT / "pdf_output"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "compile_log.txt"

# Common phrases that indicate the file was not successfully generated.
PLACEHOLDER_PATTERNS = ["todo", "placeholder", "no content", "tbd"]


def log(filename: str, status: str, reason: str = "") -> None:
    """Append a log entry to the compile log."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().isoformat(timespec="seconds")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        if reason:
            f.write(f"{timestamp} | {filename} | {status} | {reason}\n")
        else:
            f.write(f"{timestamp} | {filename} | {status}\n")


def has_placeholder(text: str) -> bool:
    lowered = text.strip().lower()
    return any(pat in lowered for pat in PLACEHOLDER_PATTERNS)


def validate_markdown(text: str, min_chars: int) -> Tuple[bool, str]:
    """Perform sanity checks on Markdown content."""

    if not text.strip():
        return False, "empty file"
    if len(text) < min_chars:
        return False, "too short"
    if has_placeholder(text):
        return False, "placeholder content"

    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        return False, "missing title header"
    if sum(1 for l in lines if l.startswith("## ")) < 2:
        return False, "missing sections"

    if text.count("```") % 2 != 0:
        return False, "unclosed code block"
    if text.count("$$") % 2 != 0:
        return False, "unbalanced $$"
    if text.count(r"\[") != text.count(r"\]"):
        return False, "unbalanced \\[\\]"
    if text.count(r"\(") != text.count(r"\)"):
        return False, "unbalanced \\(\\)"
    if text.count("$") % 2 != 0:
        return False, "unbalanced $"

    return True, ""


INLINE_LATEX_RE = re.compile(r"(?<![$\\\\])\\(frac|sqrt|alpha|beta|gamma|pi|theta|sum|int|lim)")


def preprocess_markdown(text: str) -> str:
    """Normalize inline math and fix simple syntax issues."""

    # Convert Obsidian-style math: \( ... \) -> $...$
    text = text.replace("\\(", "$").replace("\\)", "$")

    # Wrap bare LaTeX commands with $...$ if they're likely math.
    def repl(match: re.Match[str]) -> str:
        return f"${match.group(0)}$"

    text = INLINE_LATEX_RE.sub(repl, text)

    # Ensure code fences are balanced by appending a closing block if needed.
    if text.count("```") % 2 != 0:
        text += "\n```"

    return text


def compile_markdown(path: Path, *, dry_run: bool, force: bool, min_chars: int) -> Tuple[bool, str]:
    """Validate, preprocess and compile a single Markdown file."""

    content = path.read_text(encoding="utf-8")
    ok, reason = validate_markdown(content, min_chars)
    if not ok:
        return False, reason

    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = PDF_OUTPUT_DIR / f"{path.stem}.pdf"
    if pdf_path.exists() and not force:
        return True, "already exists"

    if dry_run:
        return True, "dry run"

    processed = preprocess_markdown(content)

    with NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(processed)
        tmp_path = Path(tmp.name)

    cmd = [
        "pandoc",
        str(tmp_path),
        "-o",
        str(pdf_path),
        "--pdf-engine=pdflatex",
        "-V",
        "mainfont=Latin Modern Roman",
        "-V",
        "geometry:margin=1in",
        "--quiet",
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        tmp_path.unlink(missing_ok=True)
        err = e.stderr.decode("utf-8", "ignore").strip()
        return False, f"pandoc error: {err}" or "pandoc error"
    tmp_path.unlink(missing_ok=True)
    return True, ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile Markdown files to PDFs")
    parser.add_argument("--dry-run", action="store_true", help="Show files but do not compile")
    parser.add_argument("--file", help="Compile a single Markdown file")
    parser.add_argument("--all", action="store_true", help="Force recompilation even if PDFs exist")
    parser.add_argument(
        "--min-chars",
        type=int,
        default=100,
        help="Minimum characters required to compile a file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = [OUTPUT_DIR / args.file] if args.file else sorted(OUTPUT_DIR.glob("*.md"))

    success = failure = 0
    for md_file in files:
        if not md_file.exists():
            log(md_file.name, "❌ Failure", "file not found")
            print(f"Missing {md_file.name}")
            failure += 1
            continue

        ok, reason = compile_markdown(
            md_file, dry_run=args.dry_run, force=args.all, min_chars=args.min_chars
        )
        if ok:
            log(md_file.name, "✅ Success", reason)
            msg = "Would compile" if args.dry_run else "Compiled"
            if reason == "already exists":
                msg = "Skipping"
            print(f"{msg} {md_file.name}{' (' + reason + ')' if reason else ''}")
            success += 1
        else:
            log(md_file.name, "❌ Failure", reason)
            print(f"Failed {md_file.name}: {reason}")
            failure += 1

    print(f"✅ {success} successful, ❌ {failure} failed")


if __name__ == "__main__":
    main()

