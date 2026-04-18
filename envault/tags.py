"""Tag support for grouping and filtering vault variables."""
from __future__ import annotations
import json
from pathlib import Path

DEFAULT_TAGS_FILE = Path(".envault_tags.json")


def _load_tags(tags_file: Path = DEFAULT_TAGS_FILE) -> dict[str, list[str]]:
    if not tags_file.exists():
        return {}
    with tags_file.open() as f:
        return json.load(f)


def _save_tags(tags: dict[str, list[str]], tags_file: Path = DEFAULT_TAGS_FILE) -> None:
    with tags_file.open("w") as f:
        json.dump(tags, f, indent=2)


def add_tag(key: str, tag: str, tags_file: Path = DEFAULT_TAGS_FILE) -> None:
    tags = _load_tags(tags_file)
    entry = tags.setdefault(key, [])
    if tag not in entry:
        entry.append(tag)
    _save_tags(tags, tags_file)


def remove_tag(key: str, tag: str, tags_file: Path = DEFAULT_TAGS_FILE) -> None:
    tags = _load_tags(tags_file)
    if key in tags and tag in tags[key]:
        tags[key].remove(tag)
        if not tags[key]:
            del tags[key]
    _save_tags(tags, tags_file)


def get_tags(key: str, tags_file: Path = DEFAULT_TAGS_FILE) -> list[str]:
    return _load_tags(tags_file).get(key, [])


def keys_by_tag(tag: str, tags_file: Path = DEFAULT_TAGS_FILE) -> list[str]:
    tags = _load_tags(tags_file)
    return [k for k, v in tags.items() if tag in v]


def clear_tags(key: str, tags_file: Path = DEFAULT_TAGS_FILE) -> None:
    tags = _load_tags(tags_file)
    if key in tags:
        del tags[key]
    _save_tags(tags, tags_file)


def all_tags(tags_file: Path = DEFAULT_TAGS_FILE) -> dict[str, list[str]]:
    return _load_tags(tags_file)
