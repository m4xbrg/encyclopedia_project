"""Generate LaTeX encyclopedia entries from topics CSV using OpenAI."""
from __future__ import annotations

import argparse
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import toml

from dotenv import load_dotenv
import openai
from openai import OpenAI

from utils import render_prompt, sanitize_filename

DATA_FILE = Path(__file__).resolve().parent.parent / "topics_final.csv"
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.toml"
PROMPT_TEMPLATES = {
    "definition": PROMPTS_DIR / "prompt_template_definition.txt",
    "abstract": PROMPTS_DIR / "prompt_template_abstract.txt",
    "computation": PROMPTS_DIR / "prompt_template_computation.txt",
}
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True, parents=True)
log_file = LOGS_DIR / f"generation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# Structured JSONL log accumulating across runs
JSONL_LOG_FILE = LOGS_DIR / "generation_log.jsonl"

MODEL = "gpt-4o-mini"

# Load environment variables (e.g., OPENAI_API_KEY) from .env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is missing. Please set it in the .env file.")


def generate_content(prompt: str) -> tuple[str, Optional[str]]:
    """Send prompt to OpenAI and return the response text and error message."""

    try:
        client = OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content, None
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return "Placeholder content. Replace this with real API output.", str(e)


def load_config(config_path: Path) -> tuple[int, int]:
    if not config_path.exists():
        config_path.write_text("start_index = 0\nmax_entries = 10\n", encoding="utf-8")
        print(f"Created default config at {config_path}")
    data = toml.load(config_path)
    try:
        start_index = int(data["start_index"])
        max_entries = int(data["max_entries"])
    except KeyError as e:
        raise KeyError(f"Missing '{e.args[0]}' in config.toml")
    return start_index, max_entries


def log_json(entry: dict) -> None:
    """Append a single JSON object to the JSONL log file."""

    with JSONL_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def main(enable_log: bool = True) -> None:
    template_cache: Dict[str, str] = {}
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    start_index, max_entries = load_config(CONFIG_FILE)
    df = pd.read_csv(DATA_FILE)
    end_index = start_index + max_entries
    logger.info(f"Generating entries {start_index} to {end_index}")
    topics = df.iloc[start_index:end_index].to_dict(orient="records")

    processed = successes = failures = 0

    for row in topics:
        processed += 1
        subtopic = row.get("subtopic")
        output_rel_path = (
            str(Path("output") / sanitize_filename(subtopic)) if subtopic else None
        )
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "id": row.get("id", ""),
            "domain": row.get("domain", ""),
            "topic": row.get("topic", ""),
            "subtopic": subtopic or "",
            "prompt_type": row.get("prompt_type", ""),
            "output_file": output_rel_path,
         }


        if not subtopic:
            error_msg = f"Missing subtopic in row: {row}"
            logger.error(error_msg)
            log_entry.update({"status": "error", "error_message": error_msg})
            failures += 1
            if enable_log:
                log_json(log_entry)
            continue

        prompt_type = (row.get("prompt_type") or "").strip()
        template_path = PROMPT_TEMPLATES.get(prompt_type)
        if template_path is None:
            logger.error(
                f"Unknown prompt_type '{prompt_type}' for subtopic '{subtopic}'. Using definition template.",
            )
            template_path = PROMPT_TEMPLATES["definition"]

        cache_key = str(template_path)
        template = template_cache.get(cache_key)
        if template is None:
            try:
                template = template_path.read_text(encoding="utf-8")
            except FileNotFoundError:
                error_msg = f"Prompt template not found: {template_path}"
                logger.error(f"{error_msg}. Skipping '{subtopic}'.")
                log_entry.update({"status": "error", "error_message": error_msg})
                failures += 1
                if enable_log:
                    log_json(log_entry)
                continue
            template_cache[cache_key] = template

        prompt = render_prompt(template, **row)
        content, api_error = generate_content(prompt)
        error_msg = api_error
        if not content.strip():
            error_msg = error_msg or "Empty response from API"

        header = (
            f"% {subtopic}\n"
            f"% ID: {row.get('id', '')}\n"
            f"% Domain: {row.get('domain', '')}\n"
            f"% Topic: {row.get('topic', '')}\n\n"
        )

        filename = OUTPUT_DIR / sanitize_filename(subtopic)
        if filename.exists():
            error_msg = f"File already exists, skipping: {filename}"
            logger.error(error_msg)
        else:
            filename.write_text(header + content, encoding="utf-8")
            logger.info(f"Wrote {filename}")
            print(f"Wrote {filename}")

        if error_msg:
            log_entry.update({"status": "error", "error_message": error_msg})
            failures += 1
        else:
            log_entry["status"] = "success"
            successes += 1

        if enable_log:
            log_json(log_entry)

    print(f"Processed: {processed}")
    print(f"Succeeded: {successes}")
    print(f"Failed: {failures}")
    print(f"Log file: {JSONL_LOG_FILE}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate LaTeX encyclopedia entries"
    )
    parser.add_argument(
        "--log",
        default="true",
        help="Enable structured logging (default true). Pass --log false to disable.",
    )
    args = parser.parse_args()
    enable_log = str(args.log).lower() not in {"false", "0", "no"}
    main(enable_log)
