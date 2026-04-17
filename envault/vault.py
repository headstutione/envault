"""Vault management: read/write encrypted .env files."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict

from envault.crypto import decrypt_file, encrypt_file

DEFAULT_VAULT_FILE = ".envault"


def load_vault(password: str, vault_path: str | Path = DEFAULT_VAULT_FILE) -> Dict[str, str]:
    """Decrypt and return the vault contents as a dict."""
    vault_path = Path(vault_path)
    if not vault_path.exists():
        return {}
    raw = decrypt_file(password, vault_path)
    return json.loads(raw.decode())


def save_vault(
    data: Dict[str, str],
    password: str,
    vault_path: str | Path = DEFAULT_VAULT_FILE,
) -> None:
    """Encrypt and persist the vault dict to disk."""
    vault_path = Path(vault_path)
    raw = json.dumps(data).encode()
    encrypt_file(password, raw, vault_path)


def set_variable(
    key: str,
    value: str,
    password: str,
    vault_path: str | Path = DEFAULT_VAULT_FILE,
) -> None:
    """Add or update a variable in the vault."""
    data = load_vault(password, vault_path)
    data[key] = value
    save_vault(data, password, vault_path)


def get_variable(
    key: str,
    password: str,
    vault_path: str | Path = DEFAULT_VAULT_FILE,
) -> str | None:
    """Retrieve a single variable from the vault."""
    data = load_vault(password, vault_path)
    return data.get(key)


def delete_variable(
    key: str,
    password: str,
    vault_path: str | Path = DEFAULT_VAULT_FILE,
) -> bool:
    """Remove a variable from the vault. Returns True if it existed."""
    data = load_vault(password, vault_path)
    if key not in data:
        return False
    del data[key]
    save_vault(data, password, vault_path)
    return True


def export_env(data: Dict[str, str]) -> str:
    """Convert vault dict to shell export statements."""
    lines = [f'export {k}={json.dumps(v)}' for k, v in data.items()]
    return "\n".join(lines)
