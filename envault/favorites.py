"""Manage favorite (pinned) vault keys."""
from __future__ import annotations
import json
from pathlib import Path

DEFAULT_FAVORITES_FILE = ".envault_favorites.json"


def _load_favorites(favorites_file: str = DEFAULT_FAVORITES_FILE) -> list[str]:
    p = Path(favorites_file)
    if not p.exists():
        return []
    return json.loads(p.read_text())


def _save_favorites(favorites: list[str], favorites_file: str = DEFAULT_FAVORITES_FILE) -> None:
    Path(favorites_file).write_text(json.dumps(favorites, indent=2))


def add_favorite(key: str, favorites_file: str = DEFAULT_FAVORITES_FILE) -> None:
    favorites = _load_favorites(favorites_file)
    if key in favorites:
        raise ValueError(f"Key '{key}' is already a favorite.")
    favorites.append(key)
    _save_favorites(favorites, favorites_file)


def remove_favorite(key: str, favorites_file: str = DEFAULT_FAVORITES_FILE) -> None:
    favorites = _load_favorites(favorites_file)
    if key not in favorites:
        raise KeyError(f"Key '{key}' is not a favorite.")
    favorites.remove(key)
    _save_favorites(favorites, favorites_file)


def list_favorites(favorites_file: str = DEFAULT_FAVORITES_FILE) -> list[str]:
    return _load_favorites(favorites_file)


def is_favorite(key: str, favorites_file: str = DEFAULT_FAVORITES_FILE) -> bool:
    return key in _load_favorites(favorites_file)


def clear_favorites(favorites_file: str = DEFAULT_FAVORITES_FILE) -> None:
    _save_favorites([], favorites_file)
