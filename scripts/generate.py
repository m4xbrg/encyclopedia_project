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
from tqdm import tqdm

from utils import render_prompt, slugify
from renderers import LatexRenderer, HtmlRenderer

from utils import render_prompt, slugify, normalize_artifacts, escape_latex
from registry import TemplateRegistry

from utils import render_prompt, slugify, normalize_artifacts, escape_latex, dedupe_path

# ─── Configuration & Globals ───────────────────────────────────────────────────
ROOT              = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILE = ROOT / "data" / "topics_final.csv"
PROMPTS_DIR       = ROOT / "prompts"
CONFIG_FILE       = ROOT / "config.toml"
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
def load_config(path: Path) -> tuple[int, int, Path]:
    """Load generation configuration.

    Creates ``config.toml`` with default values if it does not exist and
    returns ``start_index``, ``max_entries`` and the resolved path to the
    topics CSV file.
    """
    if not path.exists():
        path.write_text(
            "start_index = 0\nmax_entries = 10\ndata_file = \"data/topics_final.csv\"\n",
            encoding="utf-8",
        )

    cfg = toml.load(path)
    data_file = ROOT / cfg.get(
        "data_file", str(DEFAULT_DATA_FILE.relative_to(ROOT))
    )
    return int(cfg["start_index"]), int(cfg["max_entries"]), data_file

# ─── Main Pipeline ────────────────────────────────────────────────────────────
def main(
    enable_log: bool = True,
    skip_existing: bool = False,
    overwrite: bool = False,
    log_format: str = "jsonl",
    metrics_file: Optional[str] = None,
    quiet: bool = False,
    fmt: str = "latex",

    start: Optional[int] = None,
    limit: Optional[int] = None,

    retries: int = 3,
  
) -> None:
    load_dotenv(ROOT / ".env")
    start_idx, max_entries, data_file = load_config(CONFIG_FILE)

    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")

    df = pd.read_csv(data_file)
    start_idx, max_entries = load_config(CONFIG_FILE)
    if start is not None:
        start_idx = start
    if limit is not None:
        max_entries = limit
    df = pd.read_csv(DATA_FILE)
    topics = df.iloc[start_idx : start_idx + max_entries].to_dict("records")

    run_start = datetime.now(timezone.utc)
    processed = success = failure = 0
    response_times = []
    for row in topics:
    renderer = LatexRenderer() if fmt == "latex" else HtmlRenderer()
    processed = success = failure = 0
    for row in tqdm(topics, disable=quiet, desc="Generating"):
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
        response_times.append(rt)
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
    total_time = (datetime.now(timezone.utc) - run_start).total_seconds()
    attempted = success + failure
    avg_rt = sum(response_times) / attempted if attempted else 0.0
    success_rate = success / attempted if attempted else 0.0
    summary = {
        "processed": processed,
        "attempted": attempted,
        "success": success,
        "failure": failure,
        "success_rate": success_rate,
        "average_response_time": avg_rt,
        "total_run_time": total_time,
    }

    print(
        "Processed: {processed}, ✓ {success}, ✗ {failure}, "
        "success rate {sr:.2%}, avg latency {rt:.2f}s, run time {tt:.2f}s".format(
            processed=processed,
            success=success,
            failure=failure,
            sr=success_rate,
            rt=avg_rt,
            tt=total_time,
        )
    )

    if enable_log:
        log_entry = {"type": "summary", **summary}
        if log_format == "jsonl":
            log_json(log_entry)
        else:
            logger.info(json.dumps(log_entry))

    if metrics_file:
        mpath = Path(metrics_file)
        mpath.parent.mkdir(parents=True, exist_ok=True)
        mpath.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    if not quiet:
        print(f"Processed: {processed}, ✓ {success}, ✗ {failure}")
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
    p.add_argument("--metrics-json", default=None,
                    help="Optional path to write run metrics as JSON")
                  default="jsonl", help="Log output format")
    p.add_argument("--quiet", action="store_true",
                  help="Suppress progress output")
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
        metrics_file = args.metrics_json,
    )

        quiet        = args.quiet,

        fmt          = args.format,
    )

        start        = args.start,
        limit        = args.limit,


        retries      = args.retries,
    )
