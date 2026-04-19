"""Dependency tracking between vault keys."""
import json
from pathlib import Path
from typing import Dict, List

DEPS_FILE = ".envault_deps.json"


def _load_deps(deps_file: str = DEPS_FILE) -> Dict[str, List[str]]:
    p = Path(deps_file)
    if not p.exists():
        return {}
    return json.loads(p.read_text())


def _save_deps(data: Dict[str, List[str]], deps_file: str = DEPS_FILE) -> None:
    Path(deps_file).write_text(json.dumps(data, indent=2))


def add_dependency(key: str, depends_on: str, deps_file: str = DEPS_FILE) -> None:
    """Record that `key` depends on `depends_on`."""
    if key == depends_on:
        raise ValueError("A key cannot depend on itself.")
    data = _load_deps(deps_file)
    deps = data.setdefault(key, [])
    if depends_on not in deps:
        deps.append(depends_on)
    _save_deps(data, deps_file)


def remove_dependency(key: str, depends_on: str, deps_file: str = DEPS_FILE) -> None:
    data = _load_deps(deps_file)
    deps = data.get(key, [])
    if depends_on not in deps:
        raise KeyError(f"Dependency '{depends_on}' not found for key '{key}'.")
    deps.remove(depends_on)
    if not deps:
        del data[key]
    _save_deps(data, deps_file)


def get_dependencies(key: str, deps_file: str = DEPS_FILE) -> List[str]:
    return _load_deps(deps_file).get(key, [])


def get_dependents(key: str, deps_file: str = DEPS_FILE) -> List[str]:
    """Return all keys that depend on `key`."""
    data = _load_deps(deps_file)
    return [k for k, deps in data.items() if key in deps]


def list_all_dependencies(deps_file: str = DEPS_FILE) -> Dict[str, List[str]]:
    return _load_deps(deps_file)


def clear_dependencies(key: str, deps_file: str = DEPS_FILE) -> None:
    data = _load_deps(deps_file)
    if key in data:
        del data[key]
    _save_deps(data, deps_file)
