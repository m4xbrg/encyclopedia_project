"""Compile LaTeX files in the output directory into PDFs using pdflatex."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Tuple
from tqdm import tqdm

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
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress progress output"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    files = [OUTPUT_DIR / args.file] if args.file else sorted(OUTPUT_DIR.glob("*.tex"))

    success = failure = 0
    results = []
    for tex_file in files:
        if not tex_file.exists():
            log(tex_file.name, "❌ Failure", "file not found")
            print(f"Missing {tex_file.name}")
            results.append(
                {
                    "file": tex_file.name,
                    "status": "failure",
                    "reason": "file not found",
                    "log": None,
                }
            )
    for tex_file in tqdm(files, disable=args.quiet, desc="Compiling"):
        if not tex_file.exists():
            log(tex_file.name, "❌ Failure", "file not found")
            if not args.quiet:
                print(f"Missing {tex_file.name}")

            logger.error("file not found: %s", tex_file.name)
            failure += 1
            continue

        ok, reason = compile_tex(tex_file, dry_run=args.dry_run, force=args.all)
        log_file = str(PDF_OUTPUT_DIR / f"{tex_file.stem}.log")
        if ok:
            log(tex_file.name, "✅ Success", reason)
            if not args.quiet:
                msg = "Would compile" if args.dry_run else "Compiled"
                if reason == "already exists":
                    msg = "Skipping"
                print(f"{msg} {tex_file.name}{' (' + reason + ')' if reason else ''}")
            success += 1
        else:
            log(tex_file.name, "❌ Failure", reason)
            if not args.quiet:
                print(f"Failed {tex_file.name}: {reason}")
            failure += 1

    if not args.quiet:
        print(f"✅ {success} successful, ❌ {failure} failed")
            msg = "Would compile" if args.dry_run else "Compiled"
            if reason == "already exists":
                msg = "Skipping"
            print(f"{msg} {tex_file.name}{' (' + reason + ')' if reason else ''}")
            results.append(
                {
                    "file": tex_file.name,
                    "status": "success",
                    "reason": reason,
                }
            )
            success += 1
        else:
            log(tex_file.name, "❌ Failure", reason)
            print(f"Failed {tex_file.name}: {reason}")
            results.append(
                {
                    "file": tex_file.name,
                    "status": "failure",
                    "reason": reason,
                    "log": log_file,
                }
            )
                logger.warning("Skipping %s (%s)", tex_file.name, reason)
            else:
                logger.info("%s %s%s", msg, tex_file.name, f" ({reason})" if reason else "")
            success += 1
        else:
            logger.error("Failed %s: %s", tex_file.name, reason)
            failure += 1

    print(f"✅ {success} successful, ❌ {failure} failed")
    return 0 if failure == 0 else 1

    logger.info("finished: %s successful, %s failed", success, failure)
 

    summary = {
        "success": [r["file"] for r in results if r["status"] == "success"],
        "failure": [
            {"file": r["file"], "reason": r["reason"], "log": r.get("log")}
            for r in results
            if r["status"] == "failure"
        ],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    import sys

    sys.exit(main())

