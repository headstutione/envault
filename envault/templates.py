"""Template support: save and apply variable templates."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_TEMPLATES_FILE = Path(".envault_templates.json")


def _load_templates(templates_file: Path) -> Dict[str, List[str]]:
    if not templates_file.exists():
        return {}
    return json.loads(templates_file.read_text())


def _save_templates(data: Dict[str, List[str]], templates_file: Path) -> None:
    templates_file.write_text(json.dumps(data, indent=2))


def create_template(name: str, keys: List[str], templates_file: Path = DEFAULT_TEMPLATES_FILE) -> None:
    """Create a named template with a list of expected keys."""
    if not keys:
        raise ValueError("Template must contain at least one key.")
    data = _load_templates(templates_file)
    if name in data:
        raise ValueError(f"Template '{name}' already exists.")
    data[name] = list(keys)
    _save_templates(data, templates_file)


def delete_template(name: str, templates_file: Path = DEFAULT_TEMPLATES_FILE) -> None:
    data = _load_templates(templates_file)
    if name not in data:
        raise KeyError(f"Template '{name}' not found.")
    del data[name]
    _save_templates(data, templates_file)


def list_templates(templates_file: Path = DEFAULT_TEMPLATES_FILE) -> Dict[str, List[str]]:
    return _load_templates(templates_file)


def get_template(name: str, templates_file: Path = DEFAULT_TEMPLATES_FILE) -> List[str]:
    data = _load_templates(templates_file)
    if name not in data:
        raise KeyError(f"Template '{name}' not found.")
    return data[name]


def check_vault_against_template(
    name: str,
    vault_keys: List[str],
    templates_file: Path = DEFAULT_TEMPLATES_FILE,
) -> Dict[str, List[str]]:
    """Return missing and extra keys compared to template."""
    template_keys = set(get_template(name, templates_file))
    vault_set = set(vault_keys)
    return {
        "missing": sorted(template_keys - vault_set),
        "extra": sorted(vault_set - template_keys),
    }
