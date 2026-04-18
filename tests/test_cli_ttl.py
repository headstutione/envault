"""Tests for envault/cli_ttl.py"""
import json
import time
import pytest
from click.testing import CliRunner
from envault.cli_ttl import ttl


@pytest.fixture
def runner(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return CliRunner()


def test_set_command_succeeds(runner):
    result = runner.invoke(ttl, ["set", "MY_KEY", "300"])
    assert result.exit_code == 0
    assert "MY_KEY" in result.output


def test_set_invalid_ttl_shows_error(runner):
    result = runner.invoke(ttl, ["set", "MY_KEY", "0"])
    assert result.exit_code == 0
    assert "Error" in result.output


def test_get_command_shows_expiry(runner):
    runner.invoke(ttl, ["set", "MY_KEY", "300"])
    result = runner.invoke(ttl, ["get", "MY_KEY"])
    assert result.exit_code == 0
    assert "MY_KEY" in result.output


def test_get_missing_key(runner):
    result = runner.invoke(ttl, ["get", "MISSING"])
    assert result.exit_code == 0
    assert "No TTL" in result.output


def test_remove_command_succeeds(runner):
    runner.invoke(ttl, ["set", "MY_KEY", "300"])
    result = runner.invoke(ttl, ["remove", "MY_KEY"])
    assert result.exit_code == 0
    assert "removed" in result.output


def test_remove_missing_key(runner):
    result = runner.invoke(ttl, ["remove", "GHOST"])
    assert result.exit_code == 0
    assert "No TTL found" in result.output


def test_list_command_empty(runner):
    result = runner.invoke(ttl, ["list"])
    assert result.exit_code == 0
    assert "No TTL" in result.output


def test_list_command_shows_keys(runner):
    runner.invoke(ttl, ["set", "A", "60"])
    runner.invoke(ttl, ["set", "B", "120"])
    result = runner.invoke(ttl, ["list"])
    assert "A" in result.output and "B" in result.output


def test_purge_command_no_expired(runner):
    runner.invoke(ttl, ["set", "FRESH", "3600"])
    result = runner.invoke(ttl, ["purge"])
    assert result.exit_code == 0
    assert "No expired" in result.output


def test_purge_command_removes_expired(runner, tmp_path):
    runner.invoke(ttl, ["set", "STALE", "3600"])
    ttl_path = tmp_path / ".envault_ttl.json"
    data = json.loads(ttl_path.read_text())
    data["STALE"] = time.time() - 10
    ttl_path.write_text(json.dumps(data))
    result = runner.invoke(ttl, ["purge"])
    assert "STALE" in result.output
