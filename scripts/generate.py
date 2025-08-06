"""Generate Markdown encyclopedia entries from topics CSV using OpenAI."""
from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Dict, Iterable

from openai import OpenAI

from utils import render_prompt, slugify

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "topics_final.csv"
TEMPLATE_FILE = Path(__file__).resolve().parent.parent / "prompts" / "template.txt"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

MODEL = "gpt-4o-mini"


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


def main() -> None:
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    for row in load_topics(DATA_FILE):
        prompt = render_prompt(template, **row)
        content = generate_content(prompt)
        filename = OUTPUT_DIR / f"{slugify(row.get('topic', 'entry'))}.md"
        filename.write_text(content, encoding="utf-8")
        print(f"Wrote {filename}")


if __name__ == "__main__":
    main()
