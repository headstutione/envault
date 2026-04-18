"""Tests for envault.rotation module."""

import json
import pytest
from pathlib import Path

from envault.vault import save_vault, load_vault
from envault.rotation import rotate_password, rekey_variable


@pytest.fixture
def vault_file(tmp_path):
    return tmp_path / ".envault.json"


@pytest.fixture
def audit_file(tmp_path):
    return tmp_path / ".envault_audit.json"


def test_rotate_password_reencrypts_all_vars(vault_file, audit_file):
    data = {"KEY1": "value1", "KEY2": "value2"}
    save_vault(vault_file, "old", data)

    count = rotate_password(vault_file, "old", "new", audit_file)

    assert count == 2
    result = load_vault(vault_file, "new")
    assert result == data


def test_rotate_password_old_password_fails(vault_file, audit_file):
    save_vault(vault_file, "correct", {"A": "1"})

    with pytest.raises(ValueError):
        rotate_password(vault_file, "wrong", "new", audit_file)


def test_rotate_password_empty_vault_raises(vault_file, audit_file):
    save_vault(vault_file, "pass", {})

    with pytest.raises(ValueError, match="empty"):
        rotate_password(vault_file, "pass", "newpass", audit_file)


def test_rotate_records_audit_event(vault_file, audit_file):
    save_vault(vault_file, "old", {"X": "y"})
    rotate_password(vault_file, "old", "new", audit_file)

    log = json.loads(audit_file.read_text())["events"]
    assert any(e["action"] == "rotate" for e in log)


def test_rekey_variable_returns_true_for_existing_key(vault_file, audit_file):
    save_vault(vault_file, "old", {"FOO": "bar", "BAZ": "qux"})

    result = rekey_variable(vault_file, "FOO", "old", "new", audit_file)

    assert result is True
    loaded = load_vault(vault_file, "new")
    assert loaded["FOO"] == "bar"


def test_rekey_variable_returns_false_for_missing_key(vault_file, audit_file):
    save_vault(vault_file, "pass", {"A": "1"})

    result = rekey_variable(vault_file, "MISSING", "pass", "newpass", audit_file)

    assert result is False
