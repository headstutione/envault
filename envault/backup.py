"""Backup and restore vault snapshots."""
from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

DEFAULT_BACKUP_DIR = Path(".envault_backups")


def create_backup(vault_path: Path, backup_dir: Path = DEFAULT_BACKUP_DIR) -> Path:
    """Copy the vault file into backup_dir with a timestamp suffix."""
    if not vault_path.exists():
        raise FileNotFoundError(f"Vault not found: {vault_path}")

    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    dest = backup_dir / f"{vault_path.stem}_{timestamp}{vault_path.suffix}"
    shutil.copy2(vault_path, dest)
    return dest


def list_backups(backup_dir: Path = DEFAULT_BACKUP_DIR) -> list[Path]:
    """Return backup files sorted oldest-first."""
    if not backup_dir.exists():
        return []
    return sorted(backup_dir.glob("*.json"))


def restore_backup(backup_path: Path, vault_path: Path) -> None:
    """Overwrite vault_path with the chosen backup snapshot."""
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup not found: {backup_path}")
    shutil.copy2(backup_path, vault_path)


def prune_backups(
    backup_dir: Path = DEFAULT_BACKUP_DIR, keep: int = 5
) -> list[Path]:
    """Delete oldest backups, keeping at most *keep* files. Returns removed paths."""
    backups = list_backups(backup_dir)
    to_remove = backups[: max(0, len(backups) - keep)]
    for p in to_remove:
        p.unlink()
    return to_remove
