"""Generate Markdown encyclopedia entries from topics CSV using OpenAI."""
from __future__ import annotations

import csv
import tomllib
from pathlib import Path
from typing import Dict, Iterable

from dotenv import load_dotenv
from openai import OpenAI

from utils import render_prompt, slugify

DATA_FILE = Path(__file__).resolve().parent.parent / "topics_final.csv"
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.toml"
PROMPT_TEMPLATES = {
    "definition": PROMPTS_DIR / "prompt_template_definition.txt",
    "abstract": PROMPTS_DIR / "prompt_template_abstract.txt",
    "computation": PROMPTS_DIR / "prompt_template_computation.txt",
}
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

MODEL = "gpt-4o-mini"

# Load environment variables (e.g., OPENAI_API_KEY) from .env
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def load_topics(csv_path: Path) -> Iterable[Dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def generate_content(prompt: str) -> str:
    """Send prompt to OpenAI and return the response text.

    Falls back to placeholder text if the API call fails (e.g., missing key).
    """
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception:
        return "Placeholder content. Replace this with real API output."


def load_config(config_path: Path) -> tuple[int, int]:
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file {config_path} not found. Please create it with 'start_index' and 'max_entries'."
        )
    with config_path.open("rb") as f:
        data = tomllib.load(f)
    try:
        start_index = int(data["start_index"])
        max_entries = int(data["max_entries"])
    except KeyError as e:
        raise KeyError(f"Missing '{e.args[0]}' in config.toml")
    return start_index, max_entries


def main() -> None:
    template_cache: Dict[str, str] = {}
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    start_index, max_entries = load_config(CONFIG_FILE)
    topics = list(load_topics(DATA_FILE))[start_index : start_index + max_entries]

    for row in topics:
        prompt_type = row.get("prompt_type")
        if not prompt_type:
            print(
                f"Error: missing prompt_type for topic '{row.get('topic', 'unknown')}'. Skipping."
            )
            continue
        try:
            template_path = PROMPT_TEMPLATES[prompt_type]
        except KeyError:
            print(
                f"Error: unknown prompt_type '{prompt_type}' for topic '{row.get('topic', 'unknown')}'. Skipping."
            )
            continue

        template = template_cache.get(prompt_type)
        if template is None:
            template = template_path.read_text(encoding="utf-8")
            template_cache[prompt_type] = template

        prompt = render_prompt(template, **row)
        content = generate_content(prompt)
        filename = OUTPUT_DIR / f"{slugify(row.get('topic', 'entry'))}.md"
        filename.write_text(content, encoding="utf-8")
        print(f"Wrote {filename}")


if __name__ == "__main__":
    main()
