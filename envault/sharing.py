"""Team sharing support: export/import encrypted vault bundles."""

import json
import base64
from pathlib import Path
from typing import Optional

from envault.crypto import encrypt, decrypt
from envault.vault import load_vault, save_vault

BUNDLE_VERSION = 1


def export_bundle(vault_path: Path, password: str, output_path: Path) -> None:
    """Export vault as an encrypted shareable bundle."""
    vault = load_vault(vault_path)
    if not vault:
        raise ValueError("Vault is empty — nothing to export.")

    plaintext = json.dumps(vault).encode()
    ciphertext = encrypt(plaintext, password)

    bundle = {
        "version": BUNDLE_VERSION,
        "data": base64.b64encode(ciphertext).decode(),
    }

    output_path.write_text(json.dumps(bundle, indent=2))


def import_bundle(
    bundle_path: Path,
    password: str,
    vault_path: Path,
    overwrite: bool = False,
) -> dict:
    """Import an encrypted bundle into the vault.

    Returns a dict with keys 'added' and 'skipped'.
    """
    raw = bundle_path.read_text()
    bundle = json.loads(raw)

    if bundle.get("version") != BUNDLE_VERSION:
        raise ValueError(f"Unsupported bundle version: {bundle.get('version')}")

    ciphertext = base64.b64decode(bundle["data"])
    plaintext = decrypt(ciphertext, password)  # raises ValueError on bad password
    incoming: dict = json.loads(plaintext.decode())

    existing = load_vault(vault_path)
    added, skipped = [], []

    for key, value in incoming.items():
        if key in existing and not overwrite:
            skipped.append(key)
        else:
            existing[key] = value
            added.append(key)

    save_vault(vault_path, existing)
    return {"added": added, "skipped": skipped}
