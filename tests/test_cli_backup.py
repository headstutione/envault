"""Tests for envault.cli_backup."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from envault.cli_backup import backup


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture()
def vault_and_bdir(tmp_path):
    """Create a vault file and backup directory for reuse across tests."""
    vault = tmp_path / ".envault.json"
    vault.write_text(json.dumps({"K": "v"}))
    bdir = tmp_path / "bk"
    return vault, bdir


def test_create_command_succeeds(runner, tmp_path):
    vault = tmp_path / ".envault.json"
    vault.write_text(json.dumps({"A": "1"}))
    bdir = tmp_path / "bk"
    result = runner.invoke(
        backup, ["create", "--vault", str(vault), "--backup-dir", str(bdir)]
    )
    assert result.exit_code == 0
    assert "Backup created" in result.output


def test_create_missing_vault_shows_error(runner, tmp_path):
    result = runner.invoke(
        backup,
        ["create", "--vault", str(tmp_path / "no.json"), "--backup-dir", str(tmp_path)],
    )
    assert result.exit_code != 0
    assert "Error" in result.output


def test_list_command_empty(runner, tmp_path):
    result = runner.invoke(backup, ["list", "--backup-dir", str(tmp_path / "bk")])
    assert result.exit_code == 0
    assert "No backups found" in result.output


def test_list_command_shows_files(runner, tmp_path):
    vault = tmp_path / ".envault.json"
    vault.write_text(json.dumps({"X": "y"}))
    bdir = tmp_path / "bk"
    runner.invoke(backup, ["create", "--vault", str(vault), "--backup-dir", str(bdir)])
    result = runner.invoke(backup, ["list", "--backup-dir", str(bdir)])
    assert result.exit_code == 0
    assert ".json" in result.output


def test_restore_command_succeeds(runner, tmp_path):
    vault = tmp_path / ".envault.json"
    vault.write_text(json.dumps({"K": "v"}))
    bdir = tmp_path / "bk"
    runner.invoke(backup, ["create", "--vault", str(vault), "--backup-dir", str(bdir)])
    backup_file = sorted(bdir.glob("*.json"))[0]
    new_vault = tmp_path / "restored.json"
    result = runner.invoke(
        backup, ["restore", str(backup_file), "--vault", str(new_vault)]
    )
    assert result.exit_code == 0
    assert "restored" in result.output


def test_restore_preserves_content(runner, vault_and_bdir, tmp_path):
    """Verify that restored vault file contains the original data."""
    vault, bdir = vault_and_bdir
    runner.invoke(backup, ["create", "--vault", str(vault), "--backup-dir", str(bdir)])
    backup_file = sorted(bdir.glob("*.json"))[0]
    new_vault = tmp_path / "restored.json"
    runner.invoke(backup, ["restore", str(backup_file), "--vault", str(new_vault)])
    assert new_vault.exists()
    assert json.loads(new_vault.read_text()) == {"K": "v"}


def test_prune_command(runner, tmp_path):
    vault = tmp_path / ".envault.json"
    vault.write_text(json.dumps({"K": "v"}))
    bdir = tmp_path / "bk"
    for _ in range(4):
        runner.invoke(backup, ["create", "--vault", str(vault), "--backup-dir", str(bdir)])
    result = runner.invoke(backup, ["prune", "--keep", "2", "--backup-dir", str(bdir)])
    assert result.exit_code == 0
    assert len(list(bdir.glob("*.json"))) == 2
