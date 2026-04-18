"""Variable change history tracking for envault."""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Optional

DEFAULT_HISTORY_FILE = Path(".envault_history.json")


def _load_history(history_file: Path) -> dict:
    if not history_file.exists():
        return {}
    with history_file.open("r") as f:
        return json.load(f)


def _save_history(data: dict, history_file: Path) -> None:
    with history_file.open("w") as f:
        json.dump(data, f, indent=2)


def record_change(key: str, action: str, history_file: Path = DEFAULT_HISTORY_FILE) -> None:
    """Record a set/delete action for a key."""
    data = _load_history(history_file)
    if key not in data:
        data[key] = []
    data[key].append({"action": action, "timestamp": time.time()})
    _save_history(data, history_file)


def get_history(key: str, history_file: Path = DEFAULT_HISTORY_FILE) -> list:
    """Return list of change events for a key."""
    data = _load_history(history_file)
    return data.get(key, [])


def clear_history(key: Optional[str] = None, history_file: Path = DEFAULT_HISTORY_FILE) -> None:
    """Clear history for a specific key or all keys."""
    if key is None:
        _save_history({}, history_file)
    else:
        data = _load_history(history_file)
        data.pop(key, None)
        _save_history(data, history_file)


def list_changed_keys(history_file: Path = DEFAULT_HISTORY_FILE) -> list:
    """Return all keys that have history entries."""
    return list(_load_history(history_file).keys())
