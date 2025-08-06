"""Compile Markdown files in the output directory into a single PDF."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path

import markdown
from pypdf import PdfReader, PdfWriter
from weasyprint import HTML

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
PDF_PATH = Path(__file__).resolve().parent.parent / "compiled.pdf"


def markdown_to_pdf_bytes(text: str) -> bytes:
    html = markdown.markdown(text)
    return HTML(string=html).write_pdf()


def main() -> None:
    writer = PdfWriter()

    for md_file in sorted(OUTPUT_DIR.glob("*.md")):
        pdf_bytes = markdown_to_pdf_bytes(md_file.read_text(encoding="utf-8"))
        reader = PdfReader(BytesIO(pdf_bytes))
        for page in reader.pages:
            writer.add_page(page)

    with PDF_PATH.open("wb") as f:
        writer.write(f)
    print(f"Created {PDF_PATH}")


if __name__ == "__main__":
    main()
