"""Profile management: named sets of variables (e.g. dev, staging, prod)."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_PROFILES_FILE = Path(".envault_profiles.json")


def _load_profiles(profiles_file: Path = DEFAULT_PROFILES_FILE) -> Dict[str, List[str]]:
    if not profiles_file.exists():
        return {}
    return json.loads(profiles_file.read_text())


def _save_profiles(data: Dict[str, List[str]], profiles_file: Path = DEFAULT_PROFILES_FILE) -> None:
    profiles_file.write_text(json.dumps(data, indent=2))


def create_profile(name: str, profiles_file: Path = DEFAULT_PROFILES_FILE) -> None:
    data = _load_profiles(profiles_file)
    if name in data:
        raise ValueError(f"Profile '{name}' already exists.")
    data[name] = []
    _save_profiles(data, profiles_file)


def delete_profile(name: str, profiles_file: Path = DEFAULT_PROFILES_FILE) -> None:
    data = _load_profiles(profiles_file)
    if name not in data:
        raise KeyError(f"Profile '{name}' not found.")
    del data[name]
    _save_profiles(data, profiles_file)


def assign_key(name: str, key: str, profiles_file: Path = DEFAULT_PROFILES_FILE) -> None:
    data = _load_profiles(profiles_file)
    if name not in data:
        raise KeyError(f"Profile '{name}' not found.")
    if key not in data[name]:
        data[name].append(key)
    _save_profiles(data, profiles_file)


def unassign_key(name: str, key: str, profiles_file: Path = DEFAULT_PROFILES_FILE) -> None:
    data = _load_profiles(profiles_file)
    if name not in data:
        raise KeyError(f"Profile '{name}' not found.")
    data[name] = [k for k in data[name] if k != key]
    _save_profiles(data, profiles_file)


def get_profile_keys(name: str, profiles_file: Path = DEFAULT_PROFILES_FILE) -> List[str]:
    data = _load_profiles(profiles_file)
    if name not in data:
        raise KeyError(f"Profile '{name}' not found.")
    return list(data[name])


def list_profiles(profiles_file: Path = DEFAULT_PROFILES_FILE) -> List[str]:
    return list(_load_profiles(profiles_file).keys())
