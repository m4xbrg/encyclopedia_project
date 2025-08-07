# generate.py
from __future__ import annotations

import argparse
import json
from logger import get_logger
import os
import re
from datetime import datetime, timezone
from hashlib import sha1
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import toml
from dotenv import load_dotenv
from openai import OpenAI

from utils import render_prompt, slugify, normalize_artifacts, escape_latex

# ─── Configuration & Globals ───────────────────────────────────────────────────
ROOT           = Path(__file__).resolve().parent.parent
DATA_FILE      = ROOT / "topics_final.csv"
PROMPTS_DIR    = ROOT / "prompts"
CONFIG_FILE    = ROOT / "config.toml"
OUTPUT_DIR     = ROOT / "output"
LOGS_DIR       = ROOT / "logs"
JSONL_LOG_FILE = LOGS_DIR / "generation_log.jsonl"

PROMPT_TEMPLATES = {
    "definition":  PROMPTS_DIR / "prompt_template_definition.txt",
    "abstract":    PROMPTS_DIR / "prompt_template_abstract.txt",
    "computation": PROMPTS_DIR / "prompt_template_computation.txt",
}

TEX_WRAPPER = r"""
\documentclass[12pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage{{amsmath, amssymb}}
\usepackage{{geometry}}
\usepackage{{titlesec}}
\usepackage{{hyperref}}
\geometry{{margin=1in}}

\titleformat{{\section}}[block]{{\large\bfseries}}{{}}{{0em}}{{}}
\titleformat{{\subsection}}[block]{{\normalsize\bfseries}}{{}}{{0em}}{{}}

\begin{{document}}

% Title: {title}
% ID: {id}
% Domain: {domain}
% Topic: {topic}

{body}

\end{{document}}
"""

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
def generate_content(prompt: str) -> tuple[str, Optional[str]]:
    """Call OpenAI and return (content, error_message)."""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content, None
    except Exception as e:
        logger.error(f"API error: {e}")
        return "%% placeholder content due to API error %%", str(e)

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
    math_pat = re.compile(r"\\\$.*?\\\$|\\\\\[.*?\\\\\]", re.DOTALL)
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
) -> None:
    load_dotenv(ROOT / ".env")
    start_idx, max_entries = load_config(CONFIG_FILE)
    df = pd.read_csv(DATA_FILE)
    topics = df.iloc[start_idx : start_idx + max_entries].to_dict("records")

    processed = success = failure = 0
    for row in topics:
        processed += 1
        sec_id   = row.get("section_id") or row.get("id")
        domain   = row.get("domain", "TBD")
        topic    = row.get("topic", "")
        subtopic = row.get("subtopic", "")
        ptype    = (row.get("prompt_type") or "definition").strip()

        # Build filename: domain-topic-subtopic.tex
        d = slugify(domain); t = slugify(topic); s = slugify(subtopic)
        filename = OUTPUT_DIR / f"{d}-{t}-{s}.tex"
        OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

        # Prep log entry
        entry: Dict[str, any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "id": sec_id,
            "prompt_type": ptype,
        }

        # Skip/Overwrite logic
        if filename.exists() and not overwrite:
            status = "skipped"
            reason = "exists"
            if skip_existing:
                entry.update({"status": status, "reason": reason})
                if enable_log and log_format == "jsonl": log_json(entry)
                continue
            else:
                entry.update({"status": status, "reason": reason})
                if enable_log and log_format == "jsonl": log_json(entry)
                continue

        # Render prompt
        tpl = PROMPT_TEMPLATES.get(ptype, PROMPT_TEMPLATES["definition"])
        template = tpl.read_text(encoding="utf-8")
        prompt = render_prompt(template, **row)

        # Call API
        start = datetime.now(timezone.utc)
        content, err = generate_content(prompt)
        rt = (datetime.now(timezone.utc) - start).total_seconds()

        # Convert & wrap
        body    = convert_markdown_to_latex(content)
        wrapped = TEX_WRAPPER.format(
            title=topic, id=sec_id, domain=domain, topic=topic, body=body
        )

        # Compute hash & finalize log entry
        ch = sha1(wrapped.encode("utf-8")).hexdigest()
        entry.update({
            "filename": filename.name,
            "content_hash": ch,
            "api_response_time": rt,
            "status": "error" if err else "success",
        })
        if err:
            entry["error_message"] = err
            failure += 1
        else:
            success += 1

        # Write file
        filename.write_text(wrapped, encoding="utf-8")

        # Emit log
        if enable_log:
            if log_format == "jsonl":
                log_json(entry)
            else:
                logger.info(json.dumps(entry))

    logger.info(
        "processed summary: %s total, %s succeeded, %s failed",
        processed,
        success,
        failure,
    )

# ─── CLI Flags ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate LaTeX entries")
    p.add_argument("--log", default="true",
                  help="Enable structured logging")
    p.add_argument("--skip-existing", action="store_true",
                  help="Skip if .tex exists")
    p.add_argument("--overwrite", action="store_true",
                  help="Overwrite existing .tex")
    p.add_argument("--log-format", choices=["jsonl","text"],
                  default="jsonl", help="Log output format")

    args = p.parse_args()
    _enable = str(args.log).lower() not in {"false","0","no"}

    main(
        enable_log   = _enable,
        skip_existing= args.skip_existing,
        overwrite    = args.overwrite,
        log_format   = args.log_format,
    )
