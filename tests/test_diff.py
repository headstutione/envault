import pytest
from pathlib import Path
from envault.vault import set_variable
from envault.diff import diff_vaults, diff_vault_dotenv, DiffEntry

PASSWORD = "testpass"


@pytest.fixture
def vault_a(tmp_path):
    p = tmp_path / "vault_a.json"
    set_variable(p, "KEY1", "value1", PASSWORD)
    set_variable(p, "SHARED", "same", PASSWORD)
    set_variable(p, "CHANGED", "old", PASSWORD)
    return p


@pytest.fixture
def vault_b(tmp_path):
    p = tmp_path / "vault_b.json"
    set_variable(p, "KEY2", "value2", PASSWORD)
    set_variable(p, "SHARED", "same", PASSWORD)
    set_variable(p, "CHANGED", "new", PASSWORD)
    return p


def test_diff_vaults_added(vault_a, vault_b):
    entries = diff_vaults(vault_a, PASSWORD, vault_b, PASSWORD)
    statuses = {e.key: e.status for e in entries}
    assert statuses["KEY2"] == "added"


def test_diff_vaults_removed(vault_a, vault_b):
    entries = diff_vaults(vault_a, PASSWORD, vault_b, PASSWORD)
    statuses = {e.key: e.status for e in entries}
    assert statuses["KEY1"] == "removed"


def test_diff_vaults_changed(vault_a, vault_b):
    entries = diff_vaults(vault_a, PASSWORD, vault_b, PASSWORD)
    statuses = {e.key: e.status for e in entries}
    assert statuses["CHANGED"] == "changed"
    entry = next(e for e in entries if e.key == "CHANGED")
    assert entry.left == "old"
    assert entry.right == "new"


def test_diff_vaults_unchanged(vault_a, vault_b):
    entries = diff_vaults(vault_a, PASSWORD, vault_b, PASSWORD)
    statuses = {e.key: e.status for e in entries}
    assert statuses["SHARED"] == "unchanged"


def test_diff_vault_dotenv(tmp_path, vault_a):
    dotenv = tmp_path / ".env"
    dotenv.write_text('SHARED=same\nNEWKEY="hello"\n')
    entries = diff_vault_dotenv(vault_a, PASSWORD, dotenv)
    statuses = {e.key: e.status for e in entries}
    assert statuses["NEWKEY"] == "added"
    assert statuses["SHARED"] == "unchanged"
    assert statuses["KEY1"] == "removed"


def test_diff_empty_vaults(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    set_variable(a, "X", "1", PASSWORD)
    set_variable(b, "X", "1", PASSWORD)
    entries = diff_vaults(a, PASSWORD, b, PASSWORD)
    assert all(e.status == "unchanged" for e in entries)
