"""Tests for envault.backup."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from envault.backup import create_backup, list_backups, restore_backup, prune_backups


@pytest.fixture()
def vault_file(tmp_path: Path) -> Path:
    p = tmp_path / ".envault.json"
    p.write_text(json.dumps({"KEY": "value"}))
    return p


@pytest.fixture()
def backup_dir(tmp_path: Path) -> Path:
    return tmp_path / "backups"


def test_create_backup_returns_path(vault_file, backup_dir):
    dest = create_backup(vault_file, backup_dir)
    assert dest.exists()
    assert dest.suffix == ".json"


def test_create_backup_content_matches(vault_file, backup_dir):
    dest = create_backup(vault_file, backup_dir)
    assert dest.read_text() == vault_file.read_text()


def test_create_backup_missing_vault_raises(tmp_path, backup_dir):
    with pytest.raises(FileNotFoundError):
        create_backup(tmp_path / "missing.json", backup_dir)


def test_list_backups_empty_when_no_dir(tmp_path):
    assert list_backups(tmp_path / "nonexistent") == []


def test_list_backups_returns_sorted(vault_file, backup_dir):
    b1 = create_backup(vault_file, backup_dir)
    b2 = create_backup(vault_file, backup_dir)
    listed = list_backups(backup_dir)
    assert len(listed) == 2
    assert listed[0].name <= listed[1].name


def test_restore_backup_overwrites_vault(vault_file, backup_dir, tmp_path):
    dest = create_backup(vault_file, backup_dir)
    new_vault = tmp_path / "new.json"
    restore_backup(dest, new_vault)
    assert new_vault.read_text() == vault_file.read_text()


def test_restore_missing_backup_raises(tmp_path, vault_file):
    with pytest.raises(FileNotFoundError):
        restore_backup(tmp_path / "ghost.json", vault_file)


def test_prune_keeps_n_most_recent(vault_file, backup_dir):
    for _ in range(7):
        create_backup(vault_file, backup_dir)
    removed = prune_backups(backup_dir, keep=3)
    assert len(removed) == 4
    assert len(list_backups(backup_dir)) == 3


def test_prune_no_op_when_under_limit(vault_file, backup_dir):
    create_backup(vault_file, backup_dir)
    removed = prune_backups(backup_dir, keep=5)
    assert removed == []
