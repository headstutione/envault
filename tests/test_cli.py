import pytest
from click.testing import CliRunner
from envault.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_set_and_get_variable(runner, tmp_path):
    vault = str(tmp_path / "vault")
    result = runner.invoke(cli, ["--vault", vault, "set", "API_KEY", "secret123"], input="pass\npass\n")
    assert result.exit_code == 0
    assert "Set 'API_KEY' successfully." in result.output

    result = runner.invoke(cli, ["--vault", vault, "get", "API_KEY", "--password", "pass"])
    assert result.exit_code == 0
    assert "secret123" in result.output


def test_get_missing_key(runner, tmp_path):
    vault = str(tmp_path / "vault")
    runner.invoke(cli, ["--vault", vault, "set", "X", "1"], input="pass\npass\n")
    result = runner.invoke(cli, ["--vault", vault, "get", "MISSING", "--password", "pass"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_delete_variable(runner, tmp_path):
    vault = str(tmp_path / "vault")
    runner.invoke(cli, ["--vault", vault, "set", "TO_DEL", "val"], input="pass\npass\n")
    result = runner.invoke(cli, ["--vault", vault, "delete", "TO_DEL", "--password", "pass"])
    assert result.exit_code == 0
    assert "Deleted 'TO_DEL'" in result.output


def test_delete_missing_key(runner, tmp_path):
    vault = str(tmp_path / "vault")
    runner.invoke(cli, ["--vault", vault, "set", "X", "1"], input="pass\npass\n")
    result = runner.invoke(cli, ["--vault", vault, "delete", "NOPE", "--password", "pass"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_list_variables(runner, tmp_path):
    vault = str(tmp_path / "vault")
    runner.invoke(cli, ["--vault", vault, "set", "KEY1", "v1"], input="pass\npass\n")
    runner.invoke(cli, ["--vault", vault, "set", "KEY2", "v2"], input="pass\npass\n")
    result = runner.invoke(cli, ["--vault", vault, "list", "--password", "pass"])
    assert result.exit_code == 0
    assert "KEY1" in result.output
    assert "KEY2" in result.output


def test_list_empty_vault(runner, tmp_path):
    vault = str(tmp_path / "vault")
    runner.invoke(cli, ["--vault", vault, "set", "K", "v"], input="pass\npass\n")
    runner.invoke(cli, ["--vault", vault, "delete", "K", "--password", "pass"])
    result = runner.invoke(cli, ["--vault", vault, "list", "--password", "pass"])
    assert result.exit_code == 0
    assert "empty" in result.output


def test_wrong_password_on_get(runner, tmp_path):
    vault = str(tmp_path / "vault")
    runner.invoke(cli, ["--vault", vault, "set", "K", "v"], input="pass\npass\n")
    result = runner.invoke(cli, ["--vault", vault, "get", "K", "--password", "wrong"])
    assert result.exit_code != 0
