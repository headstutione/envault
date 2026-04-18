"""TTL (time-to-live) expiry management for vault variables."""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Optional

DEFAULT_TTL_FILE = Path(".envault_ttl.json")


def _load_ttl(ttl_file: Path) -> dict:
    if not ttl_file.exists():
        return {}
    return json.loads(ttl_file.read_text())


def _save_ttl(data: dict, ttl_file: Path) -> None:
    ttl_file.write_text(json.dumps(data, indent=2))


def set_expiry(key: str, seconds: int, ttl_file: Path = DEFAULT_TTL_FILE) -> float:
    """Set expiry for a key. Returns the expiry timestamp."""
    if seconds <= 0:
        raise ValueError("TTL must be a positive integer")
    data = _load_ttl(ttl_file)
    expires_at = time.time() + seconds
    data[key] = expires_at
    _save_ttl(data, ttl_file)
    return expires_at


def get_expiry(key: str, ttl_file: Path = DEFAULT_TTL_FILE) -> Optional[float]:
    """Return expiry timestamp for key, or None if not set."""
    data = _load_ttl(ttl_file)
    return data.get(key)


def is_expired(key: str, ttl_file: Path = DEFAULT_TTL_FILE) -> bool:
    """Return True if the key has expired."""
    expiry = get_expiry(key, ttl_file)
    if expiry is None:
        return False
    return time.time() > expiry


def remove_expiry(key: str, ttl_file: Path = DEFAULT_TTL_FILE) -> bool:
    """Remove TTL for a key. Returns True if it existed."""
    data = _load_ttl(ttl_file)
    if key not in data:
        return False
    del data[key]
    _save_ttl(data, ttl_file)
    return True


def list_expiries(ttl_file: Path = DEFAULT_TTL_FILE) -> dict:
    """Return all key -> expiry timestamp mappings."""
    return _load_ttl(ttl_file)


def purge_expired(ttl_file: Path = DEFAULT_TTL_FILE) -> list[str]:
    """Remove expired entries from TTL store. Returns list of purged keys."""
    data = _load_ttl(ttl_file)
    now = time.time()
    expired = [k for k, v in data.items() if now > v]
    for k in expired:
        del data[k]
    if expired:
        _save_ttl(data, ttl_file)
    return expired
