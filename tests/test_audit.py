"""Tests for audit log module."""

import json
import pytest
from click.testing import CliRunner
from envault.audit import record_event, get_log, clear_log
from envault.cli_audit import audit


@pytest.fixture
def audit_file(tmp_path):
    return str(tmp_path / "audit.json")


def test_get_log_returns_empty_when_missing(audit_file):
    assert get_log(audit_file) == []


def test_record_event_appends_entry(audit_file):
    record_event("set", "MY_KEY", audit_file)
    log = get_log(audit_file)
    assert len(log) == 1
    assert log[0]["action"] == "set"
    assert log[0]["key"] == "MY_KEY"
    assert "timestamp" in log[0]


def test_multiple_events_accumulate(audit_file):
    record_event("set", "A", audit_file)
    record_event("get", "A", audit_file)
    record_event("delete", "A", audit_file)
    assert len(get_log(audit_file)) == 3


def test_clear_log_empties_entries(audit_file):
    record_event("set", "X", audit_file)
    clear_log(audit_file)
    assert get_log(audit_file) == []


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_log_shows_entries(runner, audit_file):
    record_event("set", "FOO", audit_file)
    result = runner.invoke(audit, ["log", "--audit-file", audit_file])
    assert result.exit_code == 0
    assert "set" in result.output
    assert "FOO" in result.output


def test_cli_log_filter_by_key(runner, audit_file):
    record_event("set", "FOO", audit_file)
    record_event("set", "BAR", audit_file)
    result = runner.invoke(audit, ["log", "--audit-file", audit_file, "--key", "FOO"])
    assert "FOO" in result.output
    assert "BAR" not in result.output


def test_cli_log_empty(runner, audit_file):
    result = runner.invoke(audit, ["log", "--audit-file", audit_file])
    assert "No audit log entries found" in result.output


def test_cli_clear_log(runner, audit_file):
    record_event("set", "Z", audit_file)
    result = runner.invoke(audit, ["clear", "--audit-file", audit_file], input="y\n")
    assert result.exit_code == 0
    assert get_log(audit_file) == []
