"""Tests for envault/snapshots.py"""
import pytest
from pathlib import Path
import envault.snapshots as snapshots


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setattr(snapshots, "SNAPSHOTS_DIR", tmp_path / ".envault_snapshots")
    monkeypatch.setattr(
        snapshots, "_index_path", lambda: tmp_path / ".envault_snapshots" / "index.json"
    )


@pytest.fixture
def vault_file(tmp_path):
    vf = tmp_path / "vault.enc"
    vf.write_bytes(b"fake-encrypted-vault-data")
    return vf


def test_create_snapshot_returns_path(vault_file):
    path = snapshots.create_snapshot(vault_file, "v1")
    assert path.exists()
    assert path.read_bytes() == b"fake-encrypted-vault-data"


def test_create_snapshot_appears_in_list(vault_file):
    snapshots.create_snapshot(vault_file, "v1")
    entries = snapshots.list_snapshots()
    assert len(entries) == 1
    assert entries[0]["name"] == "v1"


def test_list_snapshots_empty_when_missing():
    assert snapshots.list_snapshots() == []


def test_create_duplicate_snapshot_raises(vault_file):
    snapshots.create_snapshot(vault_file, "v1")
    with pytest.raises(ValueError, match="already exists"):
        snapshots.create_snapshot(vault_file, "v1")


def test_create_snapshot_missing_vault(tmp_path):
    with pytest.raises(FileNotFoundError):
        snapshots.create_snapshot(tmp_path / "nonexistent.enc", "v1")


def test_restore_snapshot_overwrites_vault(vault_file, tmp_path):
    snapshots.create_snapshot(vault_file, "v1")
    vault_file.write_bytes(b"new-data")
    snapshots.restore_snapshot("v1", vault_file)
    assert vault_file.read_bytes() == b"fake-encrypted-vault-data"


def test_restore_missing_snapshot_raises(vault_file):
    with pytest.raises(KeyError, match="not found"):
        snapshots.restore_snapshot("ghost", vault_file)


def test_delete_snapshot_removes_entry(vault_file):
    snapshots.create_snapshot(vault_file, "v1")
    snapshots.delete_snapshot("v1")
    assert snapshots.list_snapshots() == []


def test_delete_missing_snapshot_raises():
    with pytest.raises(KeyError):
        snapshots.delete_snapshot("nope")


def test_multiple_snapshots_ordered_by_creation(vault_file):
    snapshots.create_snapshot(vault_file, "alpha")
    snapshots.create_snapshot(vault_file, "beta")
    names = [s["name"] for s in snapshots.list_snapshots()]
    assert names == ["alpha", "beta"]
