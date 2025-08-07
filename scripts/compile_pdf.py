"""Validate generated entries and optionally compile them into a single PDF."""
from __future__ import annotations

import argparse
import csv
import subprocess
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Tuple

from pypdf import PdfReader, PdfWriter

from utils import slugify


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"
TOPICS_FILE = ROOT / "topics_final.csv"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "validation_report.txt"
PDF_PATH = ROOT / "compiled.pdf"


def load_prompt_types(csv_path: Path) -> Dict[str, str]:
    """Return a mapping of slugified subtopic to prompt type."""
    mapping: Dict[str, str] = {}
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping[slugify(row["subtopic"])] = row["prompt_type"].strip()
    return mapping


def validate_entry(file_path: Path, prompt_type: str) -> Tuple[bool, str]:
    """Validate a file's contents based on the prompt type."""
    text = file_path.read_text(encoding="utf-8")

    if prompt_type == "abstract":
        expected = [f"## {i}." for i in range(1, 5)]
        missing = [h for h in expected if h not in text]
        if missing:
            return False, f"Missing section: {', '.join(missing)}"
        return True, ""

    if prompt_type == "definition":
        required = [
            "\\section*{",
            "\\subsection*{Definition}",
            "\\subsection*{Worked Example}",
            "\\subsection*{Common Pitfalls}",
        ]
        missing = [s for s in required if s not in text]
        if missing:
            return False, f"Missing section: {', '.join(missing)}"
        return True, ""

    if prompt_type == "computation":
        missing = []
        if "\\begin{align*}" not in text:
            missing.append("\\begin{align*}")
        if "\\subsection*{Worked Example}" not in text:
            missing.append("\\subsection*{Worked Example}")
        if "\\subsection*{Common Mistakes}" not in text and "\\subsection*{Common Pitfalls}" not in text:
            missing.append("\\subsection*{Common Mistakes}")
        if missing:
            return False, f"Missing section: {', '.join(missing)}"
        return True, ""

    return False, f"Unknown prompt type: {prompt_type}"


def convert_to_pdf_bytes(path: Path) -> bytes:
    """Convert a Markdown or LaTeX file to PDF bytes."""
    with TemporaryDirectory() as tmpdir:
        tmp_pdf = Path(tmpdir) / "out.pdf"
        if path.suffix == ".md":
            subprocess.run(["pandoc", str(path), "-o", str(tmp_pdf)], check=True)
        elif path.suffix == ".tex":
            subprocess.run(["tectonic", str(path), "--outdir", tmpdir], check=True)
            tmp_pdf = Path(tmpdir) / f"{path.stem}.pdf"
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        return tmp_pdf.read_bytes()


def process_files(only_validate: bool) -> None:
    prompt_map = load_prompt_types(TOPICS_FILE)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    valid_count = invalid_count = 0

    with LOG_FILE.open("w", encoding="utf-8") as log_f:
        files = sorted(OUTPUT_DIR.glob("*.md")) + sorted(OUTPUT_DIR.glob("*.tex"))
        for file_path in files:
            prompt_type = prompt_map.get(file_path.stem)
            if not prompt_type:
                log_f.write(f"{file_path.name}: Prompt type not found\n")
                invalid_count += 1
                continue

            ok, reason = validate_entry(file_path, prompt_type)
            if not ok:
                log_f.write(f"{file_path.name}: {reason}\n")
                invalid_count += 1
                continue

            valid_count += 1
            if not only_validate:
                try:
                    pdf_bytes = convert_to_pdf_bytes(file_path)
                    reader = PdfReader(BytesIO(pdf_bytes))
                    for page in reader.pages:
                        writer.add_page(page)
                except Exception as e:
                    log_f.write(f"{file_path.name}: Compilation failed: {e}\n")
                    invalid_count += 1
                    valid_count -= 1

    if not only_validate and valid_count > 0:
        with PDF_PATH.open("wb") as f:
            writer.write(f)
        print(f"Created {PDF_PATH}")

    print(f"✅ {valid_count} valid, ❌ {invalid_count} invalid")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate entries and compile to PDF")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--only-validate", action="store_true", help="Only validate files")
    group.add_argument("--compile", action="store_true", help="Validate and compile (default)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    only_validate = args.only_validate and not args.compile
    process_files(only_validate=only_validate)


if __name__ == "__main__":
    main()

