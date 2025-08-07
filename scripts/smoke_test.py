#!/usr/bin/env python3
"""Generate a dummy entry with mocked OpenAI response and ensure PDF output."""

from __future__ import annotations

import tempfile
from pathlib import Path
import sys

# Ensure project root is on the import path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import scripts.generate as gen
import scripts.compile_pdf as comp


def main() -> None:
    tmp_dir = Path(tempfile.mkdtemp())
    out_dir = tmp_dir / "output"
    pdf_dir = tmp_dir / "pdf_output"
    out_dir.mkdir()
    pdf_dir.mkdir()

    # Prepare a single dummy topic CSV
    topics_csv = tmp_dir / "topics.csv"
    topics_csv.write_text(
        "id,domain,topic,subtopic,prompt_type\n"
        "T1,TestDomain,TestTopic,Subtopic,definition\n",
        encoding="utf-8",
    )

    # Patch paths used by generate and compile modules
    gen.DATA_FILE = topics_csv
    gen.OUTPUT_DIR = out_dir
    gen.CONFIG_FILE = tmp_dir / "config.toml"
    gen.LOGS_DIR = tmp_dir / "logs"
    gen.JSONL_LOG_FILE = gen.LOGS_DIR / "generation_log.jsonl"

    comp.OUTPUT_DIR = out_dir
    comp.PDF_OUTPUT_DIR = pdf_dir
    comp.LOG_DIR = tmp_dir / "logs"
    comp.LOG_FILE = comp.LOG_DIR / "compile_log.txt"

    # Stub the OpenAI call
    def fake_generate_content(prompt: str):
        return "Stubbed content for testing.", None

    gen.generate_content = fake_generate_content

    # Run generation for the single topic
    gen.main(enable_log=False, overwrite=True)

    tex_files = list(out_dir.glob("*.tex"))
    if not tex_files:
        raise SystemExit("No LaTeX file generated")

    tex_file = tex_files[0]

    # Compile to PDF
    ok, reason = comp.compile_tex(tex_file, dry_run=False, force=True)
    if not ok:
        raise SystemExit(f"Compilation failed: {reason}")

    pdf_file = pdf_dir / f"{tex_file.stem}.pdf"
    if not pdf_file.exists():
        raise SystemExit("PDF output missing")

    print("Smoke test passed: PDF generated at", pdf_file)


if __name__ == "__main__":
    main()
