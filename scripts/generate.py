from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import pandas as pd
import toml
from dotenv import load_dotenv
from openai import OpenAI

try:
    from .utils import (
        escape_latex,
        normalize_artifacts,
        render_prompt,
        slugify,
    )
except ImportError:  # pragma: no cover
    from utils import (
        escape_latex,
        normalize_artifacts,
        render_prompt,
        slugify,
    )

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILE = ROOT / "data" / "topics_final.csv"
DATA_FILE = DEFAULT_DATA_FILE
PROMPTS_DIR = ROOT / "prompts"
PROMPT_TEMPLATES: Dict[str, Path] = {
    "definition": PROMPTS_DIR / "prompt_template_definition.txt",
    "abstract": PROMPTS_DIR / "prompt_template_abstract.txt",
    "computation": PROMPTS_DIR / "prompt_template_computation.txt",
}
CONFIG_FILE = ROOT / "config.toml"
OUTPUT_DIR = ROOT / "output"
LOGS_DIR = ROOT / "logs"
JSONL_LOG_FILE = LOGS_DIR / "generation_log.jsonl"
MODEL = "gpt-4o-mini"
TEX_WRAPPER = "\\documentclass{{article}}\n\\begin{{document}}\n{{body}}\n\\end{{document}}"

LOGS_DIR.mkdir(exist_ok=True, parents=True)


def log_json(entry: dict) -> None:
    with JSONL_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def generate_content(prompt: str, retries: int = 3) -> Tuple[Optional[str], Optional[str]]:
    """Call the OpenAI API with retries."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    for attempt in range(1, retries + 1):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content, None
        except Exception as e:  # pragma: no cover - network errors
            if attempt == retries:
                return None, str(e)
            time.sleep(2 ** attempt)
    return None, "API error"


MD_PATTERNS = [
    (re.compile(r"`([^`]+)`"), r"\\texttt{\1}"),
    (re.compile(r"\*\*(.+?)\*\*", re.DOTALL), r"\\textbf{\1}"),
    (re.compile(r"\*([^*\n]+?)\*", re.DOTALL), r"\\textit{\1}"),
]


def _replace_md(seg: str) -> str:
    for pat, repl in MD_PATTERNS:
        seg = pat.sub(repl, seg)
    return seg


def convert_markdown_to_latex(text: str) -> str:
    """Convert basic Markdown to LaTeX while preserving math blocks."""
    math_pat = re.compile(r"(?<!\\)\$(.+?)(?<!\\)\$|\\\[.*?\\\]", re.DOTALL)
    parts, last = [], 0
    for m in math_pat.finditer(text):
        raw = text[last:m.start()]
        raw = _replace_md(raw)
        raw = normalize_artifacts(raw)
        raw = escape_latex(raw)
        parts.append(raw)
        parts.append(m.group())
        last = m.end()
    tail = text[last:]
    tail = _replace_md(tail)
    tail = normalize_artifacts(tail)
    tail = escape_latex(tail)
    parts.append(tail)
    return "".join(parts)


def load_config(path: Path) -> Tuple[int, int, Path]:
    """Load configuration, creating a default file if missing."""
    if not path.exists():
        path.write_text(
            "start_index = 0\nmax_entries = 10\ndata_file = \"data/topics_final.csv\"\n",
            encoding="utf-8",
        )
    cfg = toml.load(path)
    data_file_cfg = cfg.get("data_file")
    if data_file_cfg is None:
        data_file = DATA_FILE
    else:
        data_file = (ROOT / data_file_cfg).resolve()
    return int(cfg["start_index"]), int(cfg["max_entries"]), data_file


def main(
    *,
    enable_log: bool = True,
    skip_existing: bool = False,
    overwrite: bool = False,
    log_format: str = "jsonl",
    metrics_file: str | None = None,
    quiet: bool = False,
    fmt: str = "latex",
    start: int | None = None,
    limit: int | None = None,
    retries: int = 3,
) -> int:
    """Run the generation pipeline."""
    load_dotenv()
    start_idx, max_entries, data_file = load_config(CONFIG_FILE)
    if start is not None:
        start_idx = start
    if limit is not None:
        max_entries = limit

    df = pd.read_csv(data_file)
    rows = df.iloc[start_idx : start_idx + max_entries]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    success = failure = 0
    for _, row in rows.iterrows():
        filename = OUTPUT_DIR / f"{slugify(row['domain'])}-{slugify(row['topic'])}-{slugify(row['subtopic'])}.tex"
        if filename.exists():
            if overwrite:
                pass
            elif skip_existing:
                continue
            else:
                raise FileExistsError(f"{filename} exists")
        template_path = PROMPT_TEMPLATES[row["prompt_type"]]
        template = Path(template_path).read_text(encoding="utf-8")
        prompt = render_prompt(
            template,
            domain=row["domain"],
            topic=row["topic"],
            subtopic=row["subtopic"],
        )
        content, err = generate_content(prompt)
        if content is None:
            failure += 1
            continue
        if fmt == "latex":
            body = convert_markdown_to_latex(content)
            wrapped = TEX_WRAPPER.format(body=body)
        else:
            wrapped = content
        filename.write_text(wrapped, encoding="utf-8")
        if enable_log:
            entry = {"file": filename.name, "status": "success"}
            if log_format == "jsonl":
                log_json(entry)
            else:
                print(json.dumps(entry))
        success += 1

    if metrics_file:
        Path(metrics_file).write_text(
            json.dumps({"success": success, "failure": failure}, indent=2),
            encoding="utf-8",
        )
    if not quiet:
        print(f"Processed: {len(rows)}, ✓ {success}, ✗ {failure}")
    return 0 if failure == 0 else 1


if __name__ == "__main__":
    import sys

    p = argparse.ArgumentParser(description="Generate encyclopedia entries")
    p.add_argument("--log", default="true", help="Enable structured logging")
    p.add_argument("--skip-existing", action="store_true", help="Skip if output file exists")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing output")
    p.add_argument("--log-format", choices=["jsonl", "text"], default="jsonl", help="Log output format")
    p.add_argument("--metrics-json", default=None, help="Optional path to write run metrics as JSON")
    p.add_argument("--quiet", action="store_true", help="Suppress progress output")
    p.add_argument("--format", choices=["latex", "html"], default="latex", help="Output format")
    p.add_argument("--start", type=int, help="Override start_index from config")
    p.add_argument("--limit", type=int, help="Override max_entries from config")
    p.add_argument("--retries", type=int, default=3, help="Retry count for API calls")
    args = p.parse_args()

    _enable = str(args.log).lower() not in {"false", "0", "no"}
    sys.exit(
        main(
            enable_log=_enable,
            skip_existing=args.skip_existing,
            overwrite=args.overwrite,
            log_format=args.log_format,
            metrics_file=args.metrics_json,
            quiet=args.quiet,
            fmt=args.format,
            start=args.start,
            limit=args.limit,
            retries=args.retries,
        )
    )

