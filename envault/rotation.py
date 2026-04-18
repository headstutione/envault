"""Key rotation support for envault vaults."""

import json
from pathlib import Path
from typing import Optional

from envault.crypto import encrypt, decrypt
from envault.vault import load_vault, save_vault
from envault.audit import record_event


def rotate_password(
    vault_path: Path,
    old_password: str,
    new_password: str,
    audit_path: Optional[Path] = None,
) -> int:
    """Re-encrypt all variables in the vault with a new password.

    Returns the number of variables re-encrypted.
    Raises ValueError if old_password is wrong (propagated from decrypt).
    """
    variables = load_vault(vault_path, old_password)

    if not variables:
        raise ValueError("Vault is empty — nothing to rotate.")

    save_vault(vault_path, new_password, variables)

    count = len(variables)
    record_event(
        audit_path or vault_path.parent / ".envault_audit.json",
        "rotate",
        {"keys_rotated": count},
    )
    return count


def rekey_variable(
    vault_path: Path,
    key: str,
    old_password: str,
    new_password: str,
    audit_path: Optional[Path] = None,
) -> bool:
    """Re-encrypt a single variable with a new password.

    Returns True if the key existed and was re-encrypted, False otherwise.
    """
    variables = load_vault(vault_path, old_password)

    if key not in variables:
        return False

    save_vault(vault_path, new_password, variables)

    record_event(
        audit_path or vault_path.parent / ".envault_audit.json",
        "rekey",
        {"key": key},
    )
    return True
