"""Tests for envault.history module."""
import pytest
from pathlib import Path
from envault.history import record_change, get_history, clear_history, list_changed_keys


@pytest.fixture
def history_file(tmp_path):
    return tmp_path / "history.json"


def test_get_history_returns_empty_when_missing(history_file):
    result = get_history("KEY", history_file)
    assert result == []


def test_record_change_appends_entry(history_file):
    record_change("KEY", "set", history_file)
    history = get_history("KEY", history_file)
    assert len(history) == 1
    assert history[0]["action"] == "set"
    assert "timestamp" in history[0]


def test_multiple_changes_accumulate(history_file):
    record_change("KEY", "set", history_file)
    record_change("KEY", "set", history_file)
    record_change("KEY", "delete", history_file)
    history = get_history("KEY", history_file)
    assert len(history) == 3
    assert history[-1]["action"] == "delete"


def test_different_keys_tracked_separately(history_file):
    record_change("A", "set", history_file)
    record_change("B", "set", history_file)
    record_change("B", "delete", history_file)
    assert len(get_history("A", history_file)) == 1
    assert len(get_history("B", history_file)) == 2


def test_list_changed_keys(history_file):
    record_change("X", "set", history_file)
    record_change("Y", "set", history_file)
    keys = list_changed_keys(history_file)
    assert set(keys) == {"X", "Y"}


def test_list_changed_keys_empty(history_file):
    assert list_changed_keys(history_file) == []


def test_clear_history_specific_key(history_file):
    record_change("A", "set", history_file)
    record_change("B", "set", history_file)
    clear_history("A", history_file)
    assert get_history("A", history_file) == []
    assert len(get_history("B", history_file)) == 1


def test_clear_history_all_keys(history_file):
    record_change("A", "set", history_file)
    record_change("B", "set", history_file)
    clear_history(history_file=history_file)
    assert list_changed_keys(history_file) == []
