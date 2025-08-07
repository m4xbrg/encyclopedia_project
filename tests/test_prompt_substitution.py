import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from scripts.utils import render_prompt
PROMPTS_DIR = ROOT / 'prompts'
PROMPT_FILES = [
    'prompt_template_definition.txt',
    'prompt_template_abstract.txt',
    'prompt_template_computation.txt',
]

@pytest.mark.parametrize('filename', PROMPT_FILES)
def test_prompt_placeholders_are_substituted(filename):
    template = (PROMPTS_DIR / filename).read_text(encoding='utf-8')
    result = render_prompt(template, domain='Physics', topic='Quantum Mechanics', subtopic='Entanglement')
    assert 'Physics' in result
    assert 'Quantum Mechanics' in result
    assert 'Entanglement' in result
    assert '$domain' not in result
    assert '$topic' not in result
    assert '$subtopic' not in result
