"""Group multiple keys under a named group for bulk operations."""
import json
from pathlib import Path
from typing import Dict, List

DEFAULT_GROUPS_FILE = ".envault_groups.json"


def _load_groups(groups_file: str = DEFAULT_GROUPS_FILE) -> Dict[str, List[str]]:
    p = Path(groups_file)
    if not p.exists():
        return {}
    return json.loads(p.read_text())


def _save_groups(data: Dict[str, List[str]], groups_file: str = DEFAULT_GROUPS_FILE) -> None:
    Path(groups_file).write_text(json.dumps(data, indent=2))


def create_group(name: str, keys: List[str], groups_file: str = DEFAULT_GROUPS_FILE) -> None:
    if not name:
        raise ValueError("Group name must not be empty.")
    if not keys:
        raise ValueError("Group must contain at least one key.")
    data = _load_groups(groups_file)
    if name in data:
        raise ValueError(f"Group '{name}' already exists.")
    data[name] = list(dict.fromkeys(keys))  # deduplicate, preserve order
    _save_groups(data, groups_file)


def delete_group(name: str, groups_file: str = DEFAULT_GROUPS_FILE) -> None:
    data = _load_groups(groups_file)
    if name not in data:
        raise KeyError(f"Group '{name}' not found.")
    del data[name]
    _save_groups(data, groups_file)


def add_key_to_group(name: str, key: str, groups_file: str = DEFAULT_GROUPS_FILE) -> None:
    data = _load_groups(groups_file)
    if name not in data:
        raise KeyError(f"Group '{name}' not found.")
    if key not in data[name]:
        data[name].append(key)
    _save_groups(data, groups_file)


def remove_key_from_group(name: str, key: str, groups_file: str = DEFAULT_GROUPS_FILE) -> None:
    data = _load_groups(groups_file)
    if name not in data:
        raise KeyError(f"Group '{name}' not found.")
    if key not in data[name]:
        raise KeyError(f"Key '{key}' not in group '{name}'.")
    data[name].remove(key)
    _save_groups(data, groups_file)


def get_group_keys(name: str, groups_file: str = DEFAULT_GROUPS_FILE) -> List[str]:
    data = _load_groups(groups_file)
    if name not in data:
        raise KeyError(f"Group '{name}' not found.")
    return list(data[name])


def list_groups(groups_file: str = DEFAULT_GROUPS_FILE) -> List[str]:
    return list(_load_groups(groups_file).keys())
