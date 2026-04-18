import pytest
import shutil
from pathlib import Path
from click.testing import CliRunner
from envault.cli_snapshots import snapshots
from envault.snapshots import create_snapshot


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def vault_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    vault = tmp_path / ".envault" / "vault.enc"
    vault.parent.mkdir(parents=True)
    vault.write_bytes(b"fake-vault-data")
    return vault


def test_create_command_succeeds(runner, vault_file):
    result = runner.invoke(snapshots, ["create", "--vault", str(vault_file)])
    assert result.exit_code == 0
    assert "Snapshot created" in result.output


def test_create_with_label(runner, vault_file):
    result = runner.invoke(snapshots, ["create", "--vault", str(vault_file), "--label", "before-deploy"])
    assert result.exit_code == 0
    assert "Snapshot created" in result.output


def test_create_missing_vault_shows_error(runner, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(snapshots, ["create", "--vault", str(tmp_path / "missing.enc")])
    assert result.exit_code == 0
    assert "Error" in result.output


def test_list_command_empty(runner, vault_file):
    result = runner.invoke(snapshots, ["list", "--vault", str(vault_file)])
    assert result.exit_code == 0
    assert "No snapshots found" in result.output


def test_list_command_shows_snapshots(runner, vault_file):
    create_snapshot(vault_path=str(vault_file), label="v1")
    result = runner.invoke(snapshots, ["list", "--vault", str(vault_file)])
    assert result.exit_code == 0
    assert "[v1]" in result.output


def test_restore_missing_snapshot_shows_error(runner, vault_file):
    result = runner.invoke(snapshots, ["restore", "nonexistent-id", "--vault", str(vault_file)])
    assert result.exit_code == 0
    assert "Error" in result.output


def test_delete_snapshot(runner, vault_file):
    snap_path = create_snapshot(vault_path=str(vault_file))
    from envault.snapshots import _load_index, _index_path
    index = _load_index(str(vault_file))
    snap_id = index[0]["id"]
    result = runner.invoke(snapshots, ["delete", snap_id, "--vault", str(vault_file)])
    assert result.exit_code == 0
    assert "deleted" in result.output


def test_delete_missing_snapshot_shows_error(runner, vault_file):
    result = runner.invoke(snapshots, ["delete", "bad-id", "--vault", str(vault_file)])
    assert result.exit_code == 0
    assert "Error" in result.output
