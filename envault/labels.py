"""Label management for envault variables."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List

_DEFAULT_PATH = Path(".envault_labels.json")


def _load_labels(labels_file: Path = _DEFAULT_PATH) -> Dict[str, List[str]]:
    if not labels_file.exists():
        return {}
    return json.loads(labels_file.read_text())


def _save_labels(data: Dict[str, List[str]], labels_file: Path = _DEFAULT_PATH) -> None:
    labels_file.write_text(json.dumps(data, indent=2))


def add_label(key: str, label: str, labels_file: Path = _DEFAULT_PATH) -> None:
    """Attach a label to a variable key."""
    if not label.strip():
        raise ValueError("Label must not be empty.")
    data = _load_labels(labels_file)
    existing = data.get(key, [])
    if label not in existing:
        existing.append(label)
    data[key] = existing
    _save_labels(data, labels_file)


def remove_label(key: str, label: str, labels_file: Path = _DEFAULT_PATH) -> bool:
    """Remove a label from a variable key. Returns True if removed."""
    data = _load_labels(labels_file)
    labels = data.get(key, [])
    if label not in labels:
        return False
    labels.remove(label)
    if labels:
        data[key] = labels
    else:
        data.pop(key, None)
    _save_labels(data, labels_file)
    return True


def get_labels(key: str, labels_file: Path = _DEFAULT_PATH) -> List[str]:
    """Return all labels for a key."""
    return _load_labels(labels_file).get(key, [])


def list_labels(labels_file: Path = _DEFAULT_PATH) -> Dict[str, List[str]]:
    """Return full label mapping."""
    return _load_labels(labels_file)


def find_by_label(label: str, labels_file: Path = _DEFAULT_PATH) -> List[str]:
    """Return all keys that have the given label."""
    return [k for k, v in _load_labels(labels_file).items() if label in v]
