from pathlib import Path
import sys
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from compile_pdf import compile_tex


def test_compile_tex_missing_pdflatex(tmp_path):
    tex_file = tmp_path / "sample.tex"
    tex_file.write_text("\\documentclass{article}\\begin{document}Hi\\end{document}")

    with patch("compile_pdf.subprocess.run", side_effect=FileNotFoundError()):
        with patch("compile_pdf.PDF_OUTPUT_DIR", tmp_path):
            ok, reason = compile_tex(tex_file, dry_run=False, force=False)

    assert not ok
    assert "Install TeX Live" in reason
