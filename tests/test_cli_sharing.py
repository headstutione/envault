"""Tests for sharing CLI commands."""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from envault.cli_sharing import sharing
from envault.vault import save_vault

PASSWORD = "cli-test-pass"


@pytest.fixture
def runner():
    return CliRunner()


def test_export_command_creates_file(runner, tmp_path):
    vault = tmp_path / ".envault"
    bundle = tmp_path / "out.json"
    save_vault(vault, {"FOO": "bar"})

    result = runner.invoke(
        sharing,
        ["export", str(bundle), "--password", PASSWORD, "--vault", str(vault)],
    )
    assert result.exit_code == 0
    assert bundle.exists()
    assert "exported" in result.output


def test_export_empty_vault_shows_error(runner, tmp_path):
    vault = tmp_path / ".envault"
    bundle = tmp_path / "out.json"

    result = runner.invoke(
        sharing,
        ["export", str(bundle), "--password", PASSWORD, "--vault", str(vault)],
    )
    assert result.exit_code != 0
    assert "Error" in result.output


def test_import_command_adds_keys(runner, tmp_path):
    vault = tmp_path / ".envault"
    bundle = tmp_path / "bundle.json"
    target = tmp_path / ".envault2"

    save_vault(vault, {"API": "secret"})
    runner.invoke(
        sharing,
        ["export", str(bundle), "--password", PASSWORD, "--vault", str(vault)],
    )

    result = runner.invoke(
        sharing,
        ["import", str(bundle), "--password", PASSWORD, "--vault", str(target)],
    )
    assert result.exit_code == 0
    assert "API" in result.output


def test_import_wrong_password_shows_error(runner, tmp_path):
    vault = tmp_path / ".envault"
    bundle = tmp_path / "bundle.json"
    target = tmp_path / ".envault2"

    save_vault(vault, {"KEY": "val"})
    runner.invoke(
        sharing,
        ["export", str(bundle), "--password", PASSWORD, "--vault", str(vault)],
    )

    result = runner.invoke(
        sharing,
        ["import", str(bundle), "--password", "wrong", "--vault", str(target)],
    )
    assert result.exit_code != 0
    assert "Error" in result.output
