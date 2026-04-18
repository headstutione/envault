"""Tests for envault hooks module and CLI."""
import pytest
from pathlib import Path
from click.testing import CliRunner
from envault.hooks import set_hook, remove_hook, get_hook, list_hooks
from envault.cli_hooks import hooks


@pytest.fixture
def hf(tmp_path):
    return tmp_path / "hooks.json"


@pytest.fixture
def runner():
    return CliRunner()


def test_get_hook_returns_none_when_missing(hf):
    assert get_hook("post-set", hf) is None


def test_set_and_get_hook(hf):
    set_hook("post-set", "echo done", hf)
    assert get_hook("post-set", hf) == "echo done"


def test_set_invalid_event_raises(hf):
    with pytest.raises(ValueError, match="Unknown event"):
        set_hook("on-explode", "rm -rf /", hf)


def test_remove_existing_hook(hf):
    set_hook("pre-set", "echo pre", hf)
    assert remove_hook("pre-set", hf) is True
    assert get_hook("pre-set", hf) is None


def test_remove_missing_hook_returns_false(hf):
    assert remove_hook("pre-set", hf) is False


def test_list_hooks_empty(hf):
    assert list_hooks(hf) == []


def test_list_hooks_returns_all(hf):
    set_hook("pre-set", "echo a", hf)
    set_hook("post-delete", "echo b", hf)
    result = list_hooks(hf)
    events = [e["event"] for e in result]
    assert "pre-set" in events
    assert "post-delete" in events


def test_cli_set_and_list(runner, hf):
    result = runner.invoke(hooks, ["set", "post-set", "echo hi", "--hooks-file", str(hf)])
    assert result.exit_code == 0
    assert "Hook set" in result.output
    result = runner.invoke(hooks, ["list", "--hooks-file", str(hf)])
    assert "post-set" in result.output
    assert "echo hi" in result.output


def test_cli_set_invalid_event_shows_error(runner, hf):
    result = runner.invoke(hooks, ["set", "bad-event", "cmd", "--hooks-file", str(hf)])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_cli_remove_hook(runner, hf):
    runner.invoke(hooks, ["set", "pre-delete", "echo x", "--hooks-file", str(hf)])
    result = runner.invoke(hooks, ["remove", "pre-delete", "--hooks-file", str(hf)])
    assert "removed" in result.output


def test_cli_list_empty(runner, hf):
    result = runner.invoke(hooks, ["list", "--hooks-file", str(hf)])
    assert "No hooks" in result.output
