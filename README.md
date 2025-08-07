# super_encyclopedia_rebuild

Starter project for generating LaTeX encyclopedia entries with GPT-4 and converting them into PDF files.

## Project Structure
- `data/` — place `topics_final.csv` here
- `output/` — generated LaTeX files
- `prompts/template.txt` — prompt template used for each entry
- `scripts/`
  - `generate.py` — read topics and create LaTeX entries
  - `compile_pdf.py` — validate `.tex` files and convert to PDFs using `pdflatex`
  - `utils.py` — shared helpers
- `requirements.txt` — Python dependencies

## Setup
1. Install Python 3.11+
2. `pip install -r requirements.txt`
3. Install a LaTeX distribution that provides `pdflatex`
4. Add `topics_final.csv` and fill in `prompts/template.txt`
5. Set the `OPENAI_API_KEY` environment variable

## Makefile Commands

Common tasks are provided via a Makefile:

```bash
make install  # Install Python dependencies
make build    # Generate LaTeX files and compile PDFs
make test     # Run the test suite
make clean    # Remove generated files and logs
```

## Usage
Generate LaTeX files:
```bash
python scripts/generate.py
```

Structured JSON logging with info, warning and error levels is enabled by default. To disable logging:
```bash
python scripts/generate.py --log false
```

The generator prints aggregate success/failure counts and response time
statistics when it finishes. To export these metrics for monitoring, provide a
path for the optional JSON output:

```bash
python scripts/generate.py --metrics-json logs/metrics.json
If a target `.tex` file already exists, you can control how it's handled:

* `--skip-existing` – leave existing files untouched and skip generation
* `--overwrite` – replace existing files with newly generated content

By default (without either flag), the script stops with an error if the
output file already exists. When both flags are provided, `--overwrite`
takes precedence.

Retry failed API calls (default 3 attempts):
```bash
python scripts/generate.py --retries 5
```

Compile `.tex` files into PDFs:
```bash
python scripts/compile_pdf.py          # compile all valid files
python scripts/compile_pdf.py --dry-run # preview which files would be compiled
python scripts/compile_pdf.py --file example.tex
python scripts/compile_pdf.py --all     # force recompilation of all files
```

PDFs are saved to `pdf_output/` and a structured log is written to `logs/compile_log.txt`.

