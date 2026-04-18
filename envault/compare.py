"""Compare two vault files or a vault against a .env file."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from envault.vault import load_vault, get_variable
from envault.crypto import decrypt


@dataclass
class CompareResult:
    key: str
    status: str  # 'match', 'mismatch', 'only_a', 'only_b'
    value_a: Optional[str] = None
    value_b: Optional[str] = None


def _decrypt_all(vault_path: Path, password: str) -> dict[str, str]:
    vault = load_vault(vault_path)
    result = {}
    for key, ciphertext in vault.items():
        result[key] = decrypt(bytes.fromhex(ciphertext), password)
    return result


def compare_vaults(
    vault_a: Path, password_a: str, vault_b: Path, password_b: str
) -> list[CompareResult]:
    data_a = _decrypt_all(vault_a, password_a)
    data_b = _decrypt_all(vault_b, password_b)
    all_keys = set(data_a) | set(data_b)
    results = []
    for key in sorted(all_keys):
        if key in data_a and key not in data_b:
            results.append(CompareResult(key, "only_a", value_a=data_a[key]))
        elif key in data_b and key not in data_a:
            results.append(CompareResult(key, "only_b", value_b=data_b[key]))
        elif data_a[key] == data_b[key]:
            results.append(CompareResult(key, "match", data_a[key], data_b[key]))
        else:
            results.append(CompareResult(key, "mismatch", data_a[key], data_b[key]))
    return results


def compare_vault_dotenv(
    vault_path: Path, password: str, dotenv_path: Path
) -> list[CompareResult]:
    data_a = _decrypt_all(vault_path, password)
    data_b: dict[str, str] = {}
    for line in dotenv_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        data_b[k.strip()] = v.strip().strip('"').strip("'")
    all_keys = set(data_a) | set(data_b)
    results = []
    for key in sorted(all_keys):
        if key in data_a and key not in data_b:
            results.append(CompareResult(key, "only_a", value_a=data_a[key]))
        elif key in data_b and key not in data_a:
            results.append(CompareResult(key, "only_b", value_b=data_b[key]))
        elif data_a[key] == data_b[key]:
            results.append(CompareResult(key, "match", data_a[key], data_b[key]))
        else:
            results.append(CompareResult(key, "mismatch", data_a[key], data_b[key]))
    return results
