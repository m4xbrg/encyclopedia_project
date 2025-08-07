# super_encyclopedia_rebuild

Starter project for generating Markdown encyclopedia entries with GPT-4 and compiling them into a single PDF.

## Project Structure
- `data/` — place `topics_final.csv` here
- `output/` — generated Markdown files
- `prompts/template.txt` — prompt template used for each entry
- `scripts/`
  - `generate.py` — read topics and create Markdown entries
  - `compile_pdf.py` — merge Markdown files into `compiled.pdf`
  - `utils.py` — shared helpers
- `requirements.txt` — Python dependencies

## Setup
1. Install Python 3.11+
2. `pip install -r requirements.txt`
3. Add `topics_final.csv` and fill in `prompts/template.txt`
4. Set the `OPENAI_API_KEY` environment variable

## Usage
Generate Markdown files:
```bash
python scripts/generate.py
```

Logging is enabled by default. To disable structured logging:
```bash
python scripts/generate.py --log false
```

Compile all Markdown into a single PDF:
```bash
python scripts/compile_pdf.py
```

The resulting PDF will be saved as `compiled.pdf` in the project root.
