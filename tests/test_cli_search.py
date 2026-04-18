import pytest
from click.testing import CliRunner
from envault.cli_search import search
from envault.vault import save_vault, set_variable


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def vault_file(tmp_path):
    path = str(tmp_path / ".envault")
    password = "testpass"
    vault = {}
    set_variable(vault, "DB_HOST", "localhost", password)
    set_variable(vault, "DB_PORT", "5432", password)
    set_variable(vault, "API_KEY", "secret123", password)
    save_vault(path, vault)
    return path, password


def test_list_all_keys(runner, vault_file):
    path, password = vault_file
    result = runner.invoke(search, ["list", "--vault", path, "--password", password])
    assert result.exit_code == 0
    assert "DB_HOST" in result.output
    assert "DB_PORT" in result.output
    assert "API_KEY" in result.output


def test_list_empty_vault(runner, tmp_path):
    path = str(tmp_path / ".envault")
    from envault.vault import save_vault
    save_vault(path, {})
    result = runner.invoke(search, ["list", "--vault", path, "--password", "pass"])
    assert result.exit_code == 0
    assert "empty" in result.output.lower()


def test_keys_glob_match(runner, vault_file):
    path, password = vault_file
    result = runner.invoke(search, ["keys", "DB_*", "--vault", path, "--password", password])
    assert result.exit_code == 0
    assert "DB_HOST" in result.output
    assert "DB_PORT" in result.output
    assert "API_KEY" not in result.output


def test_keys_no_match(runner, vault_file):
    path, password = vault_file
    result = runner.invoke(search, ["keys", "MISSING_*", "--vault", path, "--password", password])
    assert result.exit_code == 0
    assert "No keys matched" in result.output


def test_values_glob_match(runner, vault_file):
    path, password = vault_file
    result = runner.invoke(search, ["values", "local*", "--vault", path, "--password", password])
    assert result.exit_code == 0
    assert "DB_HOST" in result.output


def test_keys_wrong_password(runner, vault_file):
    path, _ = vault_file
    result = runner.invoke(search, ["keys", "*", "--vault", path, "--password", "wrongpass"])
    assert result.exit_code != 0
    assert "wrong password" in result.output.lower()


def test_list_missing_vault(runner, tmp_path):
    path = str(tmp_path / "nonexistent")
    result = runner.invoke(search, ["list", "--vault", path, "--password", "pass"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()
