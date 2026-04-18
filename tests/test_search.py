"""Tests for envault.search module."""
import pytest
from pathlib import Path
from envault.vault import set_variable
from envault.search import search_keys, search_values, list_keys

PASSWORD = "searchpass"


@pytest.fixture
def vault_file(tmp_path: Path) -> str:
    path = str(tmp_path / "vault.json")
    set_variable(path, PASSWORD, "DB_HOST", "localhost")
    set_variable(path, PASSWORD, "DB_PORT", "5432")
    set_variable(path, PASSWORD, "API_KEY", "secret-token")
    set_variable(path, PASSWORD, "API_SECRET", "another-secret")
    return path


def test_list_keys_returns_all(vault_file):
    keys = list_keys(vault_file)
    assert keys == sorted(["DB_HOST", "DB_PORT", "API_KEY", "API_SECRET"])


def test_list_keys_empty_vault(tmp_path):
    path = str(tmp_path / "empty.json")
    assert list_keys(path) == []


def test_search_keys_glob_prefix(vault_file):
    result = search_keys(vault_file, PASSWORD, "DB_*")
    assert set(result) == {"DB_HOST", "DB_PORT"}


def test_search_keys_glob_all(vault_file):
    result = search_keys(vault_file, PASSWORD, "*")
    assert set(result) == {"DB_HOST", "DB_PORT", "API_KEY", "API_SECRET"}


def test_search_keys_no_match(vault_file):
    result = search_keys(vault_file, PASSWORD, "REDIS_*")
    assert result == []


def test_search_keys_case_insensitive(vault_file):
    result = search_keys(vault_file, PASSWORD, "db_*", case_sensitive=False)
    assert set(result) == {"DB_HOST", "DB_PORT"}


def test_search_keys_case_sensitive_no_match(vault_file):
    result = search_keys(vault_file, PASSWORD, "db_*", case_sensitive=True)
    assert result == []


def test_search_values_substring(vault_file):
    result = search_values(vault_file, PASSWORD, "secret")
    assert set(result.keys()) == {"API_KEY", "API_SECRET"}


def test_search_values_case_insensitive(vault_file):
    result = search_values(vault_file, PASSWORD, "SECRET", case_sensitive=False)
    assert "API_KEY" in result


def test_search_values_no_match(vault_file):
    result = search_values(vault_file, PASSWORD, "nonexistent")
    assert result == {}


def test_search_values_empty_vault(tmp_path):
    path = str(tmp_path / "empty.json")
    result = search_values(path, PASSWORD, "anything")
    assert result == {}
