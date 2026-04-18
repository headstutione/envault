"""Key alias management for envault."""
import json
from pathlib import Path

DEFAULT_ALIASES_FILE = Path(".envault_aliases.json")


def _load_aliases(aliases_file: Path) -> dict:
    if not aliases_file.exists():
        return {}
    with aliases_file.open() as f:
        return json.load(f)


def _save_aliases(aliases_file: Path, data: dict) -> None:
    with aliases_file.open("w") as f:
        json.dump(data, f, indent=2)


def set_alias(key: str, alias: str, aliases_file: Path = DEFAULT_ALIASES_FILE) -> None:
    """Map an alias to a canonical key name."""
    if not key or not alias:
        raise ValueError("Key and alias must be non-empty strings.")
    data = _load_aliases(aliases_file)
    data[alias] = key
    _save_aliases(aliases_file, data)


def remove_alias(alias: str, aliases_file: Path = DEFAULT_ALIASES_FILE) -> None:
    """Remove an alias mapping."""
    data = _load_aliases(aliases_file)
    if alias not in data:
        raise KeyError(f"Alias '{alias}' not found.")
    del data[alias]
    _save_aliases(aliases_file, data)


def resolve_alias(alias: str, aliases_file: Path = DEFAULT_ALIASES_FILE) -> str:
    """Return the canonical key for an alias, or the alias itself if not mapped."""
    data = _load_aliases(aliases_file)
    return data.get(alias, alias)


def list_aliases(aliases_file: Path = DEFAULT_ALIASES_FILE) -> dict:
    """Return all alias -> key mappings."""
    return _load_aliases(aliases_file)


def aliases_for_key(key: str, aliases_file: Path = DEFAULT_ALIASES_FILE) -> list:
    """Return all aliases that point to the given key."""
    data = _load_aliases(aliases_file)
    return [alias for alias, target in data.items() if target == key]
