"""Compile LaTeX files in the output directory into PDFs using pdflatex."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Tuple

from logger import get_logger


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"
PDF_OUTPUT_DIR = ROOT / "pdf_output"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "compile_log.txt"

logger = get_logger(__name__, log_file=LOG_FILE)


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
    except FileNotFoundError:
        return False, "pdflatex not found. Install TeX Live."
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


def main() -> None:
    args = parse_args()
    files = [OUTPUT_DIR / args.file] if args.file else sorted(OUTPUT_DIR.glob("*.tex"))

    success = failure = 0
    for tex_file in files:
        if not tex_file.exists():
            logger.error("file not found: %s", tex_file.name)
            failure += 1
            continue

        ok, reason = compile_tex(tex_file, dry_run=args.dry_run, force=args.all)
        if ok:
            msg = "Would compile" if args.dry_run else "Compiled"
            if reason == "already exists":
                logger.warning("Skipping %s (%s)", tex_file.name, reason)
            else:
                logger.info("%s %s%s", msg, tex_file.name, f" ({reason})" if reason else "")
            success += 1
        else:
            logger.error("Failed %s: %s", tex_file.name, reason)
            failure += 1

    logger.info("finished: %s successful, %s failed", success, failure)


if __name__ == "__main__":
    main()

