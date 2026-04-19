import pytest
from click.testing import CliRunner
from envault.cli_groups import groups


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def gf(tmp_path):
    return str(tmp_path / "groups.json")


def test_create_and_list_group(runner, gf):
    r = runner.invoke(groups, ["create", "backend", "DB_URL", "DB_PASS", "--file", gf])
    assert r.exit_code == 0
    assert "created" in r.output

    r = runner.invoke(groups, ["list", "--file", gf])
    assert "backend" in r.output


def test_create_duplicate_shows_error(runner, gf):
    runner.invoke(groups, ["create", "g", "A", "--file", gf])
    r = runner.invoke(groups, ["create", "g", "B", "--file", gf])
    assert "Error" in r.output


def test_delete_group(runner, gf):
    runner.invoke(groups, ["create", "g", "A", "--file", gf])
    r = runner.invoke(groups, ["delete", "g", "--file", gf])
    assert "deleted" in r.output
    r = runner.invoke(groups, ["list", "--file", gf])
    assert "g" not in r.output


def test_delete_missing_group_shows_error(runner, gf):
    r = runner.invoke(groups, ["delete", "nope", "--file", gf])
    assert "Error" in r.output


def test_show_group_keys(runner, gf):
    runner.invoke(groups, ["create", "g", "KEY1", "KEY2", "--file", gf])
    r = runner.invoke(groups, ["show", "g", "--file", gf])
    assert "KEY1" in r.output
    assert "KEY2" in r.output


def test_add_and_remove_key(runner, gf):
    runner.invoke(groups, ["create", "g", "A", "--file", gf])
    r = runner.invoke(groups, ["add-key", "g", "B", "--file", gf])
    assert "added" in r.output
    r = runner.invoke(groups, ["remove-key", "g", "B", "--file", gf])
    assert "removed" in r.output


def test_list_empty_shows_message(runner, gf):
    r = runner.invoke(groups, ["list", "--file", gf])
    assert "No groups" in r.output
