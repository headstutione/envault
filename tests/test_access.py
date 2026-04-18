import pytest
from pathlib import Path
from envault.access import grant, revoke, can, list_permissions, delete_role, list_roles


@pytest.fixture
def af(tmp_path) -> Path:
    return tmp_path / "access.json"


def test_list_roles_empty_when_missing(af):
    assert list_roles(af) == []


def test_grant_creates_permission(af):
    grant("dev", "DB_PASS", "read", af)
    assert can("dev", "DB_PASS", "read", af)


def test_grant_no_duplicates(af):
    grant("dev", "DB_PASS", "read", af)
    grant("dev", "DB_PASS", "read", af)
    perms = list_permissions("dev", af)
    assert perms["DB_PASS"].count("read") == 1


def test_grant_invalid_permission_raises(af):
    with pytest.raises(ValueError, match="Invalid permission"):
        grant("dev", "DB_PASS", "execute", af)


def test_can_returns_false_for_missing_role(af):
    assert not can("admin", "SECRET", "write", af)


def test_can_returns_false_for_missing_key(af):
    grant("dev", "DB_PASS", "read", af)
    assert not can("dev", "OTHER_KEY", "read", af)


def test_revoke_removes_permission(af):
    grant("dev", "DB_PASS", "read", af)
    revoke("dev", "DB_PASS", "read", af)
    assert not can("dev", "DB_PASS", "read", af)


def test_revoke_nonexistent_is_noop(af):
    revoke("dev", "DB_PASS", "write", af)  # should not raise


def test_list_permissions_returns_all(af):
    grant("dev", "DB_PASS", "read", af)
    grant("dev", "API_KEY", "write", af)
    perms = list_permissions("dev", af)
    assert "DB_PASS" in perms
    assert "API_KEY" in perms


def test_delete_role_removes_entry(af):
    grant("dev", "DB_PASS", "read", af)
    delete_role("dev", af)
    assert "dev" not in list_roles(af)


def test_delete_missing_role_raises(af):
    with pytest.raises(KeyError, match="Role 'ghost' not found"):
        delete_role("ghost", af)


def test_multiple_roles_independent(af):
    grant("dev", "KEY", "read", af)
    grant("ops", "KEY", "write", af)
    assert can("dev", "KEY", "read", af)
    assert not can("dev", "KEY", "write", af)
    assert can("ops", "KEY", "write", af)
    assert not can("ops", "KEY", "read", af)
