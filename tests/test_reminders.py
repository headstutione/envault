import pytest
from pathlib import Path
from datetime import datetime, timezone, timedelta
from click.testing import CliRunner
from envault.reminders import set_reminder, remove_reminder, get_reminder, list_reminders, due_reminders
from envault.cli_reminders import reminders


@pytest.fixture
def rf(tmp_path):
    return tmp_path / "reminders.json"


def test_get_reminder_returns_none_when_missing(rf):
    assert get_reminder("MISSING", reminders_file=rf) is None


def test_set_and_get_reminder(rf):
    dt = datetime(2030, 1, 1, tzinfo=timezone.utc)
    set_reminder("API_KEY", dt, note="rotate soon", reminders_file=rf)
    entry = get_reminder("API_KEY", reminders_file=rf)
    assert entry is not None
    assert "2030" in entry["remind_at"]
    assert entry["note"] == "rotate soon"


def test_list_reminders_returns_all(rf):
    dt = datetime(2030, 6, 1, tzinfo=timezone.utc)
    set_reminder("A", dt, reminders_file=rf)
    set_reminder("B", dt, reminders_file=rf)
    data = list_reminders(reminders_file=rf)
    assert "A" in data and "B" in data


def test_remove_reminder(rf):
    dt = datetime(2030, 1, 1, tzinfo=timezone.utc)
    set_reminder("KEY", dt, reminders_file=rf)
    remove_reminder("KEY", reminders_file=rf)
    assert get_reminder("KEY", reminders_file=rf) is None


def test_due_reminders_past(rf):
    past = datetime(2000, 1, 1, tzinfo=timezone.utc)
    set_reminder("OLD_KEY", past, reminders_file=rf)
    due = due_reminders(reminders_file=rf)
    keys = [k for k, _ in due]
    assert "OLD_KEY" in keys


def test_due_reminders_future_not_included(rf):
    future = datetime.now(timezone.utc) + timedelta(days=30)
    set_reminder("FUTURE_KEY", future, reminders_file=rf)
    due = due_reminders(reminders_file=rf)
    keys = [k for k, _ in due]
    assert "FUTURE_KEY" not in keys


@pytest.fixture
def runner(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return CliRunner()


def test_cli_set_and_list(runner):
    result = runner.invoke(reminders, ["set", "DB_PASS", "--days", "10", "--note", "check this"])
    assert result.exit_code == 0
    assert "DB_PASS" in result.output
    result2 = runner.invoke(reminders, ["list"])
    assert "DB_PASS" in result2.output
    assert "check this" in result2.output


def test_cli_due_shows_past(runner):
    result = runner.invoke(reminders, ["set", "STALE", "--at", "2000-01-01T00:00:00+00:00"])
    assert result.exit_code == 0
    result2 = runner.invoke(reminders, ["due"])
    assert "STALE" in result2.output


def test_cli_set_missing_option_shows_error(runner):
    result = runner.invoke(reminders, ["set", "KEY"])
    assert "Error" in result.output
