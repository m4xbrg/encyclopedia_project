"""Compile LaTeX files in the output directory into PDFs using pdflatex."""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Tuple


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"
PDF_OUTPUT_DIR = ROOT / "pdf_output"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "compile_log.txt"


def log(filename: str, status: str, reason: str = "") -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().isoformat(timespec="seconds")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        if reason:
            f.write(f"{timestamp} | {filename} | {status} | {reason}\n")
        else:
            f.write(f"{timestamp} | {filename} | {status}\n")


def validate_tex(path: Path) -> Tuple[bool, str]:
    if not path.exists():
        return False, "file not found"
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return False, "empty file"
    if "\\documentclass" not in text and "\\section*{" not in text:
        return False, "missing \\documentclass or \\section*{}"
    return True, ""


def compile_tex(path: Path, *, dry_run: bool, force: bool) -> Tuple[bool, str]:
    ok, reason = validate_tex(path)
    if not ok:
        return False, reason

    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = PDF_OUTPUT_DIR / f"{path.stem}.pdf"
    if pdf_path.exists() and not force:
        return True, "already exists"

    if dry_run:
        return True, "dry run"

    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-output-directory",
        str(PDF_OUTPUT_DIR),
        str(path),
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8", "ignore").strip()
        return False, err or "pdflatex failed"

    for ext in (".aux", ".log", ".out"):
        (PDF_OUTPUT_DIR / f"{path.stem}{ext}").unlink(missing_ok=True)

    return True, ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile LaTeX files to PDFs")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show files but do not compile"
    )
    parser.add_argument("--file", help="Compile a single .tex file")
    parser.add_argument(
        "--all", action="store_true", help="Force recompilation even if PDFs exist"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = [OUTPUT_DIR / args.file] if args.file else sorted(OUTPUT_DIR.glob("*.tex"))

    success = failure = 0
    for tex_file in files:
        if not tex_file.exists():
            log(tex_file.name, "❌ Failure", "file not found")
            print(f"Missing {tex_file.name}")
            failure += 1
            continue

        ok, reason = compile_tex(tex_file, dry_run=args.dry_run, force=args.all)
        if ok:
            log(tex_file.name, "✅ Success", reason)
            msg = "Would compile" if args.dry_run else "Compiled"
            if reason == "already exists":
                msg = "Skipping"
            print(f"{msg} {tex_file.name}{' (' + reason + ')' if reason else ''}")
            success += 1
        else:
            log(tex_file.name, "❌ Failure", reason)
            print(f"Failed {tex_file.name}: {reason}")
            failure += 1

    print(f"✅ {success} successful, ❌ {failure} failed")
    return 0 if failure == 0 else 1


if __name__ == "__main__":
    import sys

    sys.exit(main())

