# super_encyclopedia_rebuild

Starter project for generating Markdown encyclopedia entries with GPT-4 and converting them into PDF files.

## Project Structure
- `data/` — place `topics_final.csv` here
- `output/` — generated Markdown files
- `prompts/template.txt` — prompt template used for each entry
- `scripts/`
  - `generate.py` — read topics and create Markdown entries
  - `compile_pdf.py` — validate Markdown and convert to PDFs
  - `utils.py` — shared helpers
- `requirements.txt` — Python dependencies

## Setup
1. Install Python 3.11+
2. `pip install -r requirements.txt`
3. Install [pandoc](https://pandoc.org) and a LaTeX distribution that provides `pdflatex`
4. Add `topics_final.csv` and fill in `prompts/template.txt`
5. Set the `OPENAI_API_KEY` environment variable

## Usage
Generate Markdown files:
```bash
python scripts/generate.py
```

Logging is enabled by default. To disable structured logging:
```bash
python scripts/generate.py --log false
```

Compile Markdown files into PDFs:
```bash
python scripts/compile_pdf.py          # compile all valid files
python scripts/compile_pdf.py --dry-run # preview which files would be compiled
python scripts/compile_pdf.py --file example.md
python scripts/compile_pdf.py --all     # force recompilation of all files
```

PDFs are saved to `pdf_output/` and a log is written to `logs/compile_log.txt`.
