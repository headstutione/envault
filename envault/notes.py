"""Per-key notes/comments storage for envault."""

import json
from pathlib import Path

DEFAULT_NOTES_FILE = ".envault_notes.json"


def _load_notes(notes_file: str = DEFAULT_NOTES_FILE) -> dict:
    p = Path(notes_file)
    if not p.exists():
        return {}
    with open(p) as f:
        return json.load(f)


def _save_notes(data: dict, notes_file: str = DEFAULT_NOTES_FILE) -> None:
    with open(notes_file, "w") as f:
        json.dump(data, f, indent=2)


def set_note(key: str, note: str, notes_file: str = DEFAULT_NOTES_FILE) -> None:
    """Attach a note to a key."""
    if not key:
        raise ValueError("Key must not be empty.")
    data = _load_notes(notes_file)
    data[key] = note
    _save_notes(data, notes_file)


def get_note(key: str, notes_file: str = DEFAULT_NOTES_FILE) -> str | None:
    """Return the note for a key, or None if not set."""
    return _load_notes(notes_file).get(key)


def remove_note(key: str, notes_file: str = DEFAULT_NOTES_FILE) -> bool:
    """Remove the note for a key. Returns True if it existed."""
    data = _load_notes(notes_file)
    if key not in data:
        return False
    del data[key]
    _save_notes(data, notes_file)
    return True


def list_notes(notes_file: str = DEFAULT_NOTES_FILE) -> dict:
    """Return all key->note mappings."""
    return _load_notes(notes_file)
