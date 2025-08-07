import unittest
from pathlib import Path

from scripts.utils import render_prompt

class PromptTemplateSubstitutionTests(unittest.TestCase):
    def setUp(self):
        self.vars = {
            "domain": "Algebra",
            "topic": "Group Theory",
            "subtopic": "Abelian Groups",
        }

    def test_templates_substitute_variables(self):
        for path in Path("prompts").glob("prompt_template_*.txt"):
            with self.subTest(template=path.name):
                template = path.read_text(encoding="utf-8")
                rendered = render_prompt(template, **self.vars)
                self.assertIn(self.vars["domain"], rendered)
                self.assertIn(self.vars["topic"], rendered)
                self.assertIn(self.vars["subtopic"], rendered)
                self.assertNotRegex(rendered, r"\[Domain\]|\[Topic\]|\[Subtopic\]")

if __name__ == "__main__":
    unittest.main()
