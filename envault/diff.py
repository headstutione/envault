"""Diff two vaults or a vault against a .env file."""
from __future__ import annotations
from pathlib import Path
from typing import NamedTuple
from envault.vault import load_vault
from envault.crypto import decrypt


class DiffEntry(NamedTuple):
    key: str
    status: str  # 'added', 'removed', 'changed', 'unchanged'
    left: str | None
    right: str | None


def _decrypt_vault(vault_path: Path, password: str) -> dict[str, str]:
    data = load_vault(vault_path)
    return {k: decrypt(v, password) for k, v in data.items()}


def diff_vaults(
    vault_a: Path, password_a: str, vault_b: Path, password_b: str
) -> list[DiffEntry]:
    """Compare two vault files and return diff entries."""
    left = _decrypt_vault(vault_a, password_a)
    right = _decrypt_vault(vault_b, password_b)
    return _compute_diff(left, right)


def diff_vault_dotenv(vault_path: Path, password: str, dotenv_path: Path) -> list[DiffEntry]:
    """Compare a vault against a .env file."""
    left = _decrypt_vault(vault_path, password)
    right = _parse_dotenv(dotenv_path)
    return _compute_diff(left, right)


def _compute_diff(left: dict[str, str], right: dict[str, str]) -> list[DiffEntry]:
    entries: list[DiffEntry] = []
    all_keys = sorted(set(left) | set(right))
    for key in all_keys:
        lv = left.get(key)
        rv = right.get(key)
        if lv is None:
            entries.append(DiffEntry(key, "added", None, rv))
        elif rv is None:
            entries.append(DiffEntry(key, "removed", lv, None))
        elif lv != rv:
            entries.append(DiffEntry(key, "changed", lv, rv))
        else:
            entries.append(DiffEntry(key, "unchanged", lv, rv))
    return entries


def _parse_dotenv(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        result[k.strip()] = v.strip().strip('"').strip("'")
    return result
