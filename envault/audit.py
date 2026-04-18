"""Audit log for vault operations."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_AUDIT_FILE = ".envault_audit.json"


def _load_log(audit_path: str) -> list:
    path = Path(audit_path)
    if not path.exists():
        return []
    with open(path, "r") as f:
        return json.load(f)


def _save_log(entries: list, audit_path: str) -> None:
    with open(audit_path, "w") as f:
        json.dump(entries, f, indent=2)


def record_event(action: str, key: str, audit_path: str = DEFAULT_AUDIT_FILE) -> None:
    """Append an audit event for the given action and key."""
    entries = _load_log(audit_path)
    entries.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "key": key,
    })
    _save_log(entries, audit_path)


def get_log(audit_path: str = DEFAULT_AUDIT_FILE) -> list:
    """Return all audit log entries."""
    return _load_log(audit_path)


def clear_log(audit_path: str = DEFAULT_AUDIT_FILE) -> None:
    """Clear the audit log."""
    _save_log([], audit_path)
