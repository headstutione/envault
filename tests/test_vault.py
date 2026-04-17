"""Tests for envault.vault module."""

import pytest
from pathlib import Path

from envault.vault import (
    delete_variable,
    export_env,
    get_variable,
    load_vault,
    save_vault,
    set_variable,
)

PASSWORD = "test-password-123"


@pytest.fixture
def vault_file(tmp_path):
    return tmp_path / ".envault"


def test_load_vault_returns_empty_dict_when_missing(vault_file):
    result = load_vault(PASSWORD, vault_file)
    assert result == {}


def test_save_and_load_roundtrip(vault_file):
    data = {"FOO": "bar", "BAZ": "qux"}
    save_vault(data, PASSWORD, vault_file)
    loaded = load_vault(PASSWORD, vault_file)
    assert loaded == data


def test_set_variable_creates_and_updates(vault_file):
    set_variable("KEY", "value1", PASSWORD, vault_file)
    assert get_variable("KEY", PASSWORD, vault_file) == "value1"

    set_variable("KEY", "value2", PASSWORD, vault_file)
    assert get_variable("KEY", PASSWORD, vault_file) == "value2"


def test_get_variable_returns_none_for_missing_key(vault_file):
    set_variable("EXISTING", "yes", PASSWORD, vault_file)
    assert get_variable("MISSING", PASSWORD, vault_file) is None


def test_delete_variable_removes_key(vault_file):
    set_variable("TO_DELETE", "bye", PASSWORD, vault_file)
    removed = delete_variable("TO_DELETE", PASSWORD, vault_file)
    assert removed is True
    assert get_variable("TO_DELETE", PASSWORD, vault_file) is None


def test_delete_variable_returns_false_when_not_found(vault_file):
    assert delete_variable("GHOST", PASSWORD, vault_file) is False


def test_wrong_password_raises_on_load(vault_file):
    save_vault({"A": "1"}, PASSWORD, vault_file)
    with pytest.raises(ValueError):
        load_vault("wrong-password", vault_file)


def test_export_env_format():
    data = {"DB_HOST": "localhost", "PORT": "5432"}
    output = export_env(data)
    assert 'export DB_HOST="localhost"' in output
    assert 'export PORT="5432"' in output
