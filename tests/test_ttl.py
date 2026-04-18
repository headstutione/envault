"""Tests for envault/ttl.py"""
import time
import pytest
from pathlib import Path
from envault.ttl import (
    set_expiry, get_expiry, is_expired, remove_expiry, list_expiries, purge_expired
)


@pytest.fixture
def ttl_file(tmp_path):
    return tmp_path / "ttl.json"


def test_get_expiry_returns_none_when_missing(ttl_file):
    assert get_expiry("KEY", ttl_file) is None


def test_set_expiry_stores_timestamp(ttl_file):
    before = time.time()
    expires_at = set_expiry("KEY", 60, ttl_file)
    after = time.time()
    assert before + 60 <= expires_at <= after + 60


def test_get_expiry_returns_stored_value(ttl_file):
    set_expiry("KEY", 100, ttl_file)
    expiry = get_expiry("KEY", ttl_file)
    assert expiry is not None
    assert expiry > time.time()


def test_is_expired_false_for_future(ttl_file):
    set_expiry("KEY", 3600, ttl_file)
    assert is_expired("KEY", ttl_file) is False


def test_is_expired_true_for_past(ttl_file):
    set_expiry("KEY", 1, ttl_file)
    # Manually backdate
    import json
    data = json.loads(ttl_file.read_text())
    data["KEY"] = time.time() - 10
    ttl_file.write_text(json.dumps(data))
    assert is_expired("KEY", ttl_file) is True


def test_is_expired_false_when_no_ttl(ttl_file):
    assert is_expired("MISSING", ttl_file) is False


def test_remove_expiry_returns_true_when_exists(ttl_file):
    set_expiry("KEY", 60, ttl_file)
    assert remove_expiry("KEY", ttl_file) is True
    assert get_expiry("KEY", ttl_file) is None


def test_remove_expiry_returns_false_when_missing(ttl_file):
    assert remove_expiry("NOPE", ttl_file) is False


def test_list_expiries_returns_all(ttl_file):
    set_expiry("A", 60, ttl_file)
    set_expiry("B", 120, ttl_file)
    data = list_expiries(ttl_file)
    assert "A" in data and "B" in data


def test_purge_expired_removes_old_entries(ttl_file):
    import json
    set_expiry("FRESH", 3600, ttl_file)
    data = json.loads(ttl_file.read_text())
    data["STALE"] = time.time() - 5
    ttl_file.write_text(json.dumps(data))
    purged = purge_expired(ttl_file)
    assert "STALE" in purged
    assert "FRESH" not in purged
    assert get_expiry("FRESH", ttl_file) is not None


def test_set_expiry_invalid_seconds(ttl_file):
    with pytest.raises(ValueError):
        set_expiry("KEY", 0, ttl_file)
