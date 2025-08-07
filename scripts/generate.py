# generate.py
from __future__ import annotations

import argparse
import json
from logger import get_logger
import os

import re
import time
from datetime import datetime, timezone
from hashlib import sha1
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import toml
from dotenv import load_dotenv
from openai import OpenAI

from utils import render_prompt, slugify
from renderers import LatexRenderer, HtmlRenderer

from utils import render_prompt, slugify, normalize_artifacts, escape_latex
from registry import TemplateRegistry

from utils import render_prompt, slugify, normalize_artifacts, escape_latex, dedupe_path

# ─── Configuration & Globals ───────────────────────────────────────────────────
ROOT           = Path(__file__).resolve().parent.parent
DATA_FILE      = ROOT / "topics_final.csv"
PROMPTS_DIR    = ROOT / "prompts"
CONFIG_FILE    = ROOT / "config.toml"
OUTPUT_DIR     = ROOT / "output"
LOGS_DIR       = ROOT / "logs"
JSONL_LOG_FILE = LOGS_DIR / "generation_log.jsonl"

TEMPLATE_REGISTRY_FILE = ROOT / "prompt_registry.toml"
TEMPLATE_REGISTRY = TemplateRegistry.from_toml(TEMPLATE_REGISTRY_FILE, ROOT)

MODEL = "gpt-4o-mini"

# ─── Logging Setup ─────────────────────────────────────────────────────────────
LOGS_DIR.mkdir(exist_ok=True, parents=True)
LOG_FILE = LOGS_DIR / f"generation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logger = get_logger(__name__, log_file=LOG_FILE)

def log_json(entry: dict) -> None:
    """Append a JSON entry to the generation log."""
    with JSONL_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# ─── Content Generation ────────────────────────────────────────────────────────
def generate_content(prompt: str, retries: int = 3) -> tuple[Optional[str], Optional[str]]:
    """Call OpenAI with retries. Returns (content, error_message)."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    for attempt in range(1, retries + 1):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content, None
        except Exception as e:
            logger.error(f"API error on attempt {attempt}/{retries}: {e}")
            if attempt == retries:
                return None, str(e)
            time.sleep(2 ** attempt)


# ─── Markdown → LaTeX Conversion ──────────────────────────────────────────────
MD_PATTERNS = [
    (re.compile(r"`([^`]+)`"),        r"\\texttt{\1}"),
    (re.compile(r"\*\*(.+?)\*\*", re.DOTALL), r"\\textbf{\1}"),
    (re.compile(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", re.DOTALL), r"\\textit{\1}"),
]

def _replace_md(seg: str) -> str:
    for pat, repl in MD_PATTERNS:
        seg = pat.sub(repl, seg)
    return seg

def convert_markdown_to_latex(text: str) -> str:
    """Convert basic Markdown to LaTeX, preserve math, then escape."""
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

# ─── Config Loader ─────────────────────────────────────────────────────────────
def load_config(path: Path) -> tuple[int, int]:
    if not path.exists():
        path.write_text("start_index = 0\nmax_entries = 10\n", encoding="utf-8")
    cfg = toml.load(path)
    return int(cfg["start_index"]), int(cfg["max_entries"])

# ─── Main Pipeline ────────────────────────────────────────────────────────────
def main(
    enable_log: bool = True,
    skip_existing: bool = False,
    overwrite: bool = False,
    log_format: str = "jsonl",
    fmt: str = "latex",

    start: Optional[int] = None,
    limit: Optional[int] = None,

    retries: int = 3,
  
) -> None:
    load_dotenv(ROOT / ".env")
    start_idx, max_entries = load_config(CONFIG_FILE)
    if start is not None:
        start_idx = start
    if limit is not None:
        max_entries = limit
    df = pd.read_csv(DATA_FILE)
    topics = df.iloc[start_idx : start_idx + max_entries].to_dict("records")

    renderer = LatexRenderer() if fmt == "latex" else HtmlRenderer()
    processed = success = failure = 0
    for row in topics:
        processed += 1
        sec_id   = row.get("section_id") or row.get("id")
        domain   = row.get("domain", "TBD")
        topic    = row.get("topic", "")
        subtopic = row.get("subtopic", "")
        ptype    = (row.get("prompt_type") or "definition").strip()

        # Determine output filename
        d = slugify(domain); t = slugify(topic); s = slugify(subtopic)
        filename = OUTPUT_DIR / f"{d}-{t}-{s}.{renderer.extension}"

        # Build filename: domain-topic-subtopic.tex
        d = slugify(domain)
        t = slugify(topic)
        s = slugify(subtopic)
        filename = OUTPUT_DIR / f"{d}-{t}-{s}.tex"
        filename = dedupe_path(filename)
        OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

        # Prep log entry
        entry: Dict[str, any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "id": sec_id,
            "prompt_type": ptype,
            "filename": filename.name,
        }

        # Skip/Overwrite logic
        if filename.exists():
            if overwrite:
                pass  # Explicit overwrite requested
            elif skip_existing:
                entry.update({"status": "skipped", "reason": "exists"})
                if enable_log and log_format == "jsonl":
                    log_json(entry)
                continue
            else:
                raise FileExistsError(
                    f"{filename} exists. Use --skip-existing to skip or --overwrite to replace."
                )

        # Render prompt via registry
        tpl = TEMPLATE_REGISTRY.get(ptype) or TEMPLATE_REGISTRY.get("definition")
        if tpl is None:
            raise KeyError(f"No template registered for '{ptype}'")
        if isinstance(tpl, Path):
            template = tpl.read_text(encoding="utf-8")
        elif callable(tpl):
            template = tpl()
        else:
            template = str(tpl)
        prompt = render_prompt(template, **row)

        # Call API
        start = datetime.now(timezone.utc)
        content, err = generate_content(prompt, retries=retries)
        rt = (datetime.now(timezone.utc) - start).total_seconds()
        entry["api_response_time"] = rt

        if err or content is None:
            entry.update({"status": "error", "error_message": err})
            failure += 1
            if enable_log:
                if log_format == "jsonl":
                    log_json(entry)
                else:
                    logger.info(json.dumps(entry))
            continue

        # Convert & wrap
        body = renderer.convert(content)
        wrapped = renderer.wrap(

        body    = convert_markdown_to_latex(content)
        wrapped = TEX_WRAPPER.format(
            title=topic, id=sec_id, domain=domain, topic=topic, body=body
        )

        ch = sha1(wrapped.encode("utf-8")).hexdigest()
        entry.update({"content_hash": ch, "status": "success"})
        filename.write_text(wrapped, encoding="utf-8")
        success += 1

        if enable_log:
            if log_format == "jsonl":
                log_json(entry)
            else:
                logger.info(json.dumps(entry))

    print(f"Processed: {processed}, ✓ {success}, ✗ {failure}")
    return 0 if failure == 0 else 1


# ─── CLI Flags ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    p = argparse.ArgumentParser(description="Generate LaTeX entries")
    logger.info(
        "processed summary: %s total, %s succeeded, %s failed",
        processed,
        success,
        failure,
    )

# ─── CLI Flags ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate entries")
    p.add_argument("--log", default="true",
                  help="Enable structured logging")
    p.add_argument("--skip-existing", action="store_true",
                  help="Skip if output file exists")
    p.add_argument("--overwrite", action="store_true",
                  help="Overwrite existing output")
    p.add_argument("--log-format", choices=["jsonl","text"],
                  default="jsonl", help="Log output format")
    p.add_argument("--format", choices=["latex", "html"],
                  default="latex", help="Output format")

    p.add_argument("--start", type=int,
                  help="Override start_index from config")
    p.add_argument("--limit", type=int,
                  help="Override max_entries from config")

    p.add_argument("--retries", type=int, default=3,
                  help="Retry count for API calls")
 


    args = p.parse_args()
    _enable = str(args.log).lower() not in {"false","0","no"}

    sys.exit(
        main(
            enable_log   = _enable,
            skip_existing= args.skip_existing,
            overwrite    = args.overwrite,
            log_format   = args.log_format,
        )
    )
    main(
        enable_log   = _enable,
        skip_existing= args.skip_existing,
        overwrite    = args.overwrite,
        log_format   = args.log_format,
        fmt          = args.format,
    )

        start        = args.start,
        limit        = args.limit,


        retries      = args.retries,
    )
