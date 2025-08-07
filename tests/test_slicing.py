import sys
from pathlib import Path

import pandas as pd

repo_root = Path(__file__).resolve().parents[1]
sys.path.extend([str(repo_root), str(repo_root / "scripts")])
import scripts.generate as gen

EXISTING_LOGS = set(Path(gen.LOGS_DIR).glob("generation_*.log"))


def setup_env(tmp_path, monkeypatch, config_start, config_limit):
    csv_path = tmp_path / "topics_final.csv"
    df = pd.DataFrame({
        "section_id": list(range(5)),
        "domain": ["d"] * 5,
        "topic": [f"topic{i}" for i in range(5)],
        "subtopic": ["sub"] * 5,
        "prompt_type": ["definition"] * 5,
    })
    df.to_csv(csv_path, index=False)

    config_path = tmp_path / "config.toml"
    config_path.write_text(
        f"start_index = {config_start}\nmax_entries = {config_limit}\n",
        encoding="utf-8",
    )

    template = tmp_path / "template.txt"
    template.write_text("Topic: $topic", encoding="utf-8")

    out_dir = tmp_path / "out"

    monkeypatch.setattr(gen, "DATA_FILE", csv_path)
    monkeypatch.setattr(gen, "CONFIG_FILE", config_path)
    monkeypatch.setattr(gen, "OUTPUT_DIR", out_dir)
    monkeypatch.setattr(gen, "PROMPT_TEMPLATES", {"definition": template})
    monkeypatch.setattr(gen, "generate_content", lambda prompt: ("content", None))

    return out_dir


def test_config_indices_used(tmp_path, monkeypatch):
    out_dir = setup_env(tmp_path, monkeypatch, 2, 2)
    gen.main(enable_log=False)
    files = sorted(p.name for p in out_dir.glob("*.tex"))
    assert files == ["d-topic2-sub.tex", "d-topic3-sub.tex"]


def test_cli_overrides_config(tmp_path, monkeypatch):
    out_dir = setup_env(tmp_path, monkeypatch, 0, 5)
    gen.main(start=1, limit=2, enable_log=False)
    files = sorted(p.name for p in out_dir.glob("*.tex"))
    assert files == ["d-topic1-sub.tex", "d-topic2-sub.tex"]


def teardown_module(module):
    for f in Path(gen.LOGS_DIR).glob("generation_*.log"):
        if f not in EXISTING_LOGS:
            try:
                f.unlink()
            except FileNotFoundError:
                pass
