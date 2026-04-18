"""Search and filter vault variables."""
from __future__ import annotations
import fnmatch
from typing import Optional
from envault.vault import load_vault, get_variable


def search_keys(
    vault_path: str,
    password: str,
    pattern: str,
    case_sensitive: bool = False,
) -> list[str]:
    """Return vault keys matching a glob pattern."""
    vault = load_vault(vault_path)
    if not vault:
        return []
    keys = list(vault.keys())
    if not case_sensitive:
        return [
            k for k in keys
            if fnmatch.fnmatchcase(k.lower(), pattern.lower())
        ]
    return [k for k in keys if fnmatch.fnmatchcase(k, pattern)]


def search_values(
    vault_path: str,
    password: str,
    substring: str,
    case_sensitive: bool = False,
) -> dict[str, str]:
    """Return keys whose decrypted values contain the given substring."""
    vault = load_vault(vault_path)
    if not vault:
        return {}
    results: dict[str, str] = {}
    for key in vault:
        value = get_variable(vault_path, password, key)
        if value is None:
            continue
        hay = value if case_sensitive else value.lower()
        needle = substring if case_sensitive else substring.lower()
        if needle in hay:
            results[key] = value
    return results


def list_keys(vault_path: str) -> list[str]:
    """Return all keys in the vault without decrypting values."""
    vault = load_vault(vault_path)
    return sorted(vault.keys())
