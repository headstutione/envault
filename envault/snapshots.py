"""Snapshot support: save and restore named vault snapshots."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

SNAPSHOTS_DIR = Path(".envault_snapshots")


def _index_path() -> Path:
    return SNAPSHOTS_DIR / "index.json"


def _load_index() -> dict:
    if not _index_path().exists():
        return {}
    return json.loads(_index_path().read_text())


def _save_index(index: dict) -> None:
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    _index_path().write_text(json.dumps(index, indent=2))


def create_snapshot(vault_path: Path, name: str) -> Path:
    if not vault_path.exists():
        raise FileNotFoundError(f"Vault not found: {vault_path}")
    index = _load_index()
    if name in index:
        raise ValueError(f"Snapshot '{name}' already exists")
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = SNAPSHOTS_DIR / f"{name}.vault"
    shutil.copy2(vault_path, dest)
    index[name] = {
        "file": dest.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _save_index(index)
    return dest


def list_snapshots() -> list[dict]:
    index = _load_index()
    return [
        {"name": name, **meta}
        for name, meta in sorted(index.items(), key=lambda x: x[1]["created_at"])
    ]


def restore_snapshot(name: str, vault_path: Path) -> None:
    index = _load_index()
    if name not in index:
        raise KeyError(f"Snapshot '{name}' not found")
    src = SNAPSHOTS_DIR / index[name]["file"]
    shutil.copy2(src, vault_path)


def delete_snapshot(name: str) -> None:
    index = _load_index()
    if name not in index:
        raise KeyError(f"Snapshot '{name}' not found")
    snap_file = SNAPSHOTS_DIR / index.pop(name)["file"]
    if snap_file.exists():
        snap_file.unlink()
    _save_index(index)
