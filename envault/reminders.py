"""Reminders: notify when variables are approaching expiry or haven't been rotated recently."""

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

DEFAULT_REMINDERS_FILE = Path(".envault_reminders.json")


def _load_reminders(reminders_file: Path) -> dict:
    if not reminders_file.exists():
        return {}
    return json.loads(reminders_file.read_text())


def _save_reminders(data: dict, reminders_file: Path) -> None:
    reminders_file.write_text(json.dumps(data, indent=2))


def set_reminder(key: str, remind_at: datetime, note: str = "", reminders_file: Path = DEFAULT_REMINDERS_FILE) -> None:
    data = _load_reminders(reminders_file)
    data[key] = {
        "remind_at": remind_at.isoformat(),
        "note": note,
    }
    _save_reminders(data, reminders_file)


def remove_reminder(key: str, reminders_file: Path = DEFAULT_REMINDERS_FILE) -> None:
    data = _load_reminders(reminders_file)
    data.pop(key, None)
    _save_reminders(data, reminders_file)


def get_reminder(key: str, reminders_file: Path = DEFAULT_REMINDERS_FILE) -> Optional[dict]:
    return _load_reminders(reminders_file).get(key)


def list_reminders(reminders_file: Path = DEFAULT_REMINDERS_FILE) -> dict:
    return _load_reminders(reminders_file)


def due_reminders(reminders_file: Path = DEFAULT_REMINDERS_FILE) -> list[tuple[str, dict]]:
    now = datetime.now(timezone.utc)
    result = []
    for key, entry in _load_reminders(reminders_file).items():
        remind_at = datetime.fromisoformat(entry["remind_at"])
        if remind_at.tzinfo is None:
            remind_at = remind_at.replace(tzinfo=timezone.utc)
        if remind_at <= now:
            result.append((key, entry))
    return result
