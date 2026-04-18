import json
import pytest
from click.testing import CliRunner
from envault.cli_history import history


@pytest.fixture
def runner():
    return CliRunner()


def _write_history(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def test_log_shows_entries(runner, tmp_path):
    hf = tmp_path / "history.json"
    _write_history(hf, {
        "DB_URL": [
            {"timestamp": "2024-01-01T00:00:00", "action": "set", "user": "alice"}
        ]
    })
    result = runner.invoke(history, ["log", "DB_URL", "--history-file", str(hf)])
    assert result.exit_code == 0
    assert "set" in result.output
    assert "alice" in result.output


def test_log_missing_key_shows_message(runner, tmp_path):
    hf = tmp_path / "history.json"
    result = runner.invoke(history, ["log", "MISSING", "--history-file", str(hf)])
    assert result.exit_code == 0
    assert "No history" in result.output


def test_clear_removes_key_history(runner, tmp_path):
    hf = tmp_path / "history.json"
    _write_history(hf, {
        "API_KEY": [
            {"timestamp": "2024-01-01T00:00:00", "action": "set", "user": "bob"}
        ]
    })
    result = runner.invoke(history, ["clear", "API_KEY", "--history-file", str(hf)], input="y\n")
    assert result.exit_code == 0
    assert "cleared" in result.output
    with open(hf) as f:
        data = json.load(f)
    assert "API_KEY" not in data


def test_list_keys_shows_all(runner, tmp_path):
    hf = tmp_path / "history.json"
    _write_history(hf, {
        "FOO": [{"timestamp": "t", "action": "set", "user": "u"}],
        "BAR": [{"timestamp": "t", "action": "delete", "user": "u"}],
    })
    result = runner.invoke(history, ["list-keys", "--history-file", str(hf)])
    assert result.exit_code == 0
    assert "FOO" in result.output
    assert "BAR" in result.output


def test_list_keys_empty(runner, tmp_path):
    hf = tmp_path / "history.json"
    result = runner.invoke(history, ["list-keys", "--history-file", str(hf)])
    assert result.exit_code == 0
    assert "No history" in result.output
