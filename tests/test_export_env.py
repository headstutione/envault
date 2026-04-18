"""Tests for envault.export_env module."""
from __future__ import annotations

import pytest
from pathlib import Path

from envault.vault import set_variable
from envault.export_env import export_dotenv, import_dotenv

PASSWORD = "test-secret"


@pytest.fixture
def vault_file(tmp_path):
    return tmp_path / "vault.json"


@pytest.fixture
def dotenv_file(tmp_path):
    return tmp_path / ".env"


def test_export_dotenv_creates_file(vault_file, dotenv_file):
    set_variable(vault_file, "API_KEY", "abc123", PASSWORD)
    count = export_dotenv(vault_file, PASSWORD, dotenv_file)
    assert count == 1
    assert dotenv_file.exists()


def test_export_dotenv_content(vault_file, dotenv_file):
    set_variable(vault_file, "DB_URL", "postgres://localhost/db", PASSWORD)
    set_variable(vault_file, "SECRET", "my\"secret", PASSWORD)
    export_dotenv(vault_file, PASSWORD, dotenv_file)
    content = dotenv_file.read_text()
    assert 'DB_URL="postgres://localhost/db"' in content
    assert 'SECRET="my\\"secret"' in content


def test_export_dotenv_empty_vault_raises(vault_file, dotenv_file):
    with pytest.raises(ValueError, match="empty"):
        export_dotenv(vault_file, PASSWORD, dotenv_file)


def test_import_dotenv_basic(vault_file, dotenv_file):
    dotenv_file.write_text('FOO="bar"\nBAZ="qux"\n')
    count = import_dotenv(vault_file, PASSWORD, dotenv_file)
    assert count == 2


def test_import_dotenv_values_correct(vault_file, dotenv_file):
    from envault.vault import get_variable
    dotenv_file.write_text('MY_VAR="hello world"\n')
    import_dotenv(vault_file, PASSWORD, dotenv_file)
    assert get_variable(vault_file, "MY_VAR", PASSWORD) == "hello world"


def test_import_dotenv_skips_comments_and_blanks(vault_file, dotenv_file):
    dotenv_file.write_text('# comment\n\nVALID="yes"\n')
    count = import_dotenv(vault_file, PASSWORD, dotenv_file)
    assert count == 1


def test_import_dotenv_missing_file_raises(vault_file, tmp_path):
    missing = tmp_path / "nonexistent.env"
    with pytest.raises(FileNotFoundError):
        import_dotenv(vault_file, PASSWORD, missing)


def test_roundtrip_export_import(vault_file, dotenv_file, tmp_path):
    from envault.vault import get_variable
    vault2 = tmp_path / "vault2.json"
    set_variable(vault_file, "ROUND", "trip_value", PASSWORD)
    export_dotenv(vault_file, PASSWORD, dotenv_file)
    import_dotenv(vault2, PASSWORD, dotenv_file)
    assert get_variable(vault2, "ROUND", PASSWORD) == "trip_value"
