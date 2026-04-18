"""Tests for envault.cli_rotation CLI commands."""

import pytest
from click.testing import CliRunner
from pathlib import Path

from envault.cli_rotation import rotation
from envault.vault import save_vault


@pytest.fixture
def runner():
    return CliRunner()


def test_rotate_command_succeeds(runner, tmp_path):
    vault = tmp_path / ".envault.json"
    save_vault(vault, "oldpass", {"KEY": "val"})

    result = runner.invoke(
        rotation,
        ["rotate", "--vault", str(vault), "--old-password", "oldpass", "--new-password", "newpass"],
    )

    assert result.exit_code == 0
    assert "Rotated 1 variable" in result.output


def test_rotate_wrong_old_password_shows_error(runner, tmp_path):
    vault = tmp_path / ".envault.json"
    save_vault(vault, "correct", {"K": "v"})

    result = runner.invoke(
        rotation,
        ["rotate", "--vault", str(vault), "--old-password", "wrong", "--new-password", "new"],
    )

    assert result.exit_code != 0
    assert "Error" in result.output


def test_rotate_missing_vault_shows_error(runner, tmp_path):
    vault = tmp_path / "nonexistent.json"

    result = runner.invoke(
        rotation,
        ["rotate", "--vault", str(vault), "--old-password", "a", "--new-password", "b"],
    )

    assert result.exit_code != 0
    assert "not found" in result.output


def test_rotate_empty_vault_shows_error(runner, tmp_path):
    vault = tmp_path / ".envault.json"
    save_vault(vault, "pass", {})

    result = runner.invoke(
        rotation,
        ["rotate", "--vault", str(vault), "--old-password", "pass", "--new-password", "new"],
    )

    assert result.exit_code != 0
    assert "Error" in result.output
