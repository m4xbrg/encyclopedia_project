import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))

spec = importlib.util.spec_from_file_location("generate", ROOT / "scripts" / "generate.py")
generate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate)


def setup_env(tmp_path, monkeypatch):
    # Paths
    data_file = tmp_path / "topics.csv"
    template_file = tmp_path / "template.txt"
    config_file = tmp_path / "config.toml"
    output_dir = tmp_path / "output"
    logs_dir = tmp_path / "logs"

    # Minimal dataset
    df = pd.DataFrame([
        {
            "section_id": 1,
            "domain": "Domain",
            "topic": "Topic",
            "subtopic": "Sub",
            "prompt_type": "definition",
        }
    ])
    df.to_csv(data_file, index=False)

    # Template
    template_file.write_text("Body for ${topic}", encoding="utf-8")

    # Config
    config_file.write_text("start_index = 0\nmax_entries = 1\n", encoding="utf-8")

    # Monkeypatch module paths
    monkeypatch.setattr(generate, "DATA_FILE", data_file)
    monkeypatch.setattr(generate, "PROMPT_TEMPLATES", {"definition": template_file})
    monkeypatch.setattr(generate, "CONFIG_FILE", config_file)
    monkeypatch.setattr(generate, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(generate, "LOGS_DIR", logs_dir)
    monkeypatch.setattr(generate, "JSONL_LOG_FILE", logs_dir / "log.jsonl")

    # Stub out heavy functions
    monkeypatch.setattr(generate, "generate_content", lambda prompt: ("new", None))
    monkeypatch.setattr(generate, "convert_markdown_to_latex", lambda text: text)
    monkeypatch.setattr(generate, "TEX_WRAPPER", "{body}")

    return output_dir / "domain-topic-sub.tex"


@pytest.mark.parametrize(
    "skip_existing, overwrite, expected",
    [
        (False, False, "error"),
        (True, False, "skip"),
        (False, True, "overwrite"),
        (True, True, "overwrite"),
    ],
)
def test_file_handling(tmp_path, monkeypatch, skip_existing, overwrite, expected):
    target = setup_env(tmp_path, monkeypatch)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("old", encoding="utf-8")

    if expected == "error":
        with pytest.raises(FileExistsError):
            generate.main(
                enable_log=False,
                skip_existing=skip_existing,
                overwrite=overwrite,
                log_format="jsonl",
            )
        assert target.read_text(encoding="utf-8") == "old"
    else:
        generate.main(
            enable_log=False,
            skip_existing=skip_existing,
            overwrite=overwrite,
            log_format="jsonl",
        )
        content = target.read_text(encoding="utf-8")
        if expected == "skip":
            assert content == "old"
        else:
            assert content == "new"
