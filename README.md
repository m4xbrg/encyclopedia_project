# super_encyclopedia_rebuild

Starter project for generating LaTeX encyclopedia entries with GPT-4 and converting them into PDF files.

## Project Structure
- `data/` — place `topics_final.csv` here (default `config.toml` expects this path)
- `output/` — generated LaTeX files
- `prompts/template.txt` — prompt template used for each entry
- `scripts/`
  - `generate.py` — read topics and create LaTeX entries
  - `compile_pdf.py` — validate `.tex` files and convert to PDFs using `pdflatex`
  - `utils.py` — shared helpers
- `config.toml` — generation settings (created automatically if missing)
- `requirements.txt` — Python dependencies

## Setup
1. Install Python 3.11+
2. `pip install -r requirements.txt`
3. Install a LaTeX distribution that provides `pdflatex`
4. Add `data/topics_final.csv` (or update `config.toml` with your CSV path) and fill in `prompts/template.txt`
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

### Generate LaTeX files
```bash
python scripts/generate.py
```

Structured logging is enabled by default. Disable it with:
```bash
python scripts/generate.py --log false
```

Export run metrics:
```bash
python scripts/generate.py --metrics-json logs/metrics.json
```

Handling existing files:

- `--skip-existing` – leave existing files untouched and skip generation
- `--overwrite` – replace existing files with newly generated content (takes precedence over `--skip-existing`)

Retry failed API calls (default 3 attempts):
```bash
python scripts/generate.py --retries 5
```

### Compile `.tex` files into PDFs
```bash
python scripts/compile_pdf.py          # compile all valid files
python scripts/compile_pdf.py --dry-run # preview which files would be compiled
python scripts/compile_pdf.py --file example.tex
python scripts/compile_pdf.py --all     # force recompilation of all files
```

PDFs are saved to `pdf_output/` and a structured log is written to `logs/compile_log.txt`.

### Run the tests
```bash
pytest
```

