import pytest
import json
from click.testing import CliRunner
from envault.notes import set_note, get_note, remove_note, list_notes
from envault.cli_notes import notes


@pytest.fixture
def nf(tmp_path):
    return str(tmp_path / "notes.json")


@pytest.fixture
def runner():
    return CliRunner()


def test_get_note_returns_none_when_missing(nf):
    assert get_note("MISSING", nf) is None


def test_set_and_get_note(nf):
    set_note("DB_URL", "Primary database connection string", nf)
    assert get_note("DB_URL", nf) == "Primary database connection string"


def test_set_note_overwrites_existing(nf):
    set_note("KEY", "old note", nf)
    set_note("KEY", "new note", nf)
    assert get_note("KEY", nf) == "new note"


def test_set_note_empty_key_raises(nf):
    with pytest.raises(ValueError):
        set_note("", "some note", nf)


def test_remove_note_returns_true_when_exists(nf):
    set_note("KEY", "note", nf)
    assert remove_note("KEY", nf) is True
    assert get_note("KEY", nf) is None


def test_remove_note_returns_false_when_missing(nf):
    assert remove_note("GHOST", nf) is False


def test_list_notes_returns_all(nf):
    set_note("A", "alpha", nf)
    set_note("B", "beta", nf)
    result = list_notes(nf)
    assert result == {"A": "alpha", "B": "beta"}


def test_list_notes_empty(nf):
    assert list_notes(nf) == {}


def test_cli_set_and_get(runner, nf):
    r = runner.invoke(notes, ["set", "API_KEY", "The main API key", "--notes-file", nf])
    assert r.exit_code == 0
    assert "Note set" in r.output
    r = runner.invoke(notes, ["get", "API_KEY", "--notes-file", nf])
    assert "The main API key" in r.output


def test_cli_get_missing(runner, nf):
    r = runner.invoke(notes, ["get", "NOPE", "--notes-file", nf])
    assert "No note found" in r.output


def test_cli_remove(runner, nf):
    runner.invoke(notes, ["set", "X", "note", "--notes-file", nf])
    r = runner.invoke(notes, ["remove", "X", "--notes-file", nf])
    assert "removed" in r.output


def test_cli_list(runner, nf):
    runner.invoke(notes, ["set", "K1", "note1", "--notes-file", nf])
    runner.invoke(notes, ["set", "K2", "note2", "--notes-file", nf])
    r = runner.invoke(notes, ["list", "--notes-file", nf])
    assert "K1" in r.output
    assert "K2" in r.output
