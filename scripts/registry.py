from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, Union

import toml

Template = Union[Path, Callable[..., str]]

class TemplateRegistry:
    """Registry mapping prompt type names to templates.

    Templates may be file paths or callables returning a template string.
    """

    def __init__(self) -> None:
        self._templates: Dict[str, Template] = {}

    def register(self, name: str, template: Template) -> None:
        """Register a template under ``name``."""
        self._templates[name] = template

    def get(self, name: str) -> Template | None:
        """Retrieve a template by ``name``."""
        return self._templates.get(name)

    @classmethod
    def from_toml(cls, path: Path, base_dir: Path | None = None) -> "TemplateRegistry":
        """Load templates from a TOML file.

        The TOML file should contain a ``[templates]`` table mapping type names
        to file paths. Paths are resolved relative to ``base_dir`` when
        provided.
        """
        registry = cls()
        if path.exists():
            data = toml.load(path)
            for name, target in data.get("templates", {}).items():
                tpl_path = Path(target)
                if base_dir and not tpl_path.is_absolute():
                    tpl_path = (base_dir / tpl_path).resolve()
                registry.register(name, tpl_path)
        return registry
