"""Tests for envault.aliases."""
import pytest
from pathlib import Path
from envault.aliases import (
    set_alias, remove_alias, resolve_alias, list_aliases, aliases_for_key
)


@pytest.fixture
def af(tmp_path):
    return tmp_path / "aliases.json"


def test_list_aliases_empty_when_missing(af):
    assert list_aliases(af) == {}


def test_set_alias_creates_mapping(af):
    set_alias("DATABASE_URL", "db", af)
    assert list_aliases(af) == {"db": "DATABASE_URL"}


def test_set_alias_overwrites_existing(af):
    set_alias("DATABASE_URL", "db", af)
    set_alias("REDIS_URL", "db", af)
    assert list_aliases(af)["db"] == "REDIS_URL"


def test_resolve_alias_returns_key(af):
    set_alias("SECRET_KEY", "secret", af)
    assert resolve_alias("secret", af) == "SECRET_KEY"


def test_resolve_alias_returns_self_when_not_mapped(af):
    assert resolve_alias("UNKNOWN", af) == "UNKNOWN"


def test_remove_alias(af):
    set_alias("API_KEY", "api", af)
    remove_alias("api", af)
    assert "api" not in list_aliases(af)


def test_remove_missing_alias_raises(af):
    with pytest.raises(KeyError):
        remove_alias("nonexistent", af)


def test_aliases_for_key_returns_all(af):
    set_alias("DATABASE_URL", "db", af)
    set_alias("DATABASE_URL", "database", af)
    set_alias("REDIS_URL", "cache", af)
    result = aliases_for_key("DATABASE_URL", af)
    assert set(result) == {"db", "database"}


def test_aliases_for_key_returns_empty_when_none(af):
    set_alias("API_KEY", "api", af)
    assert aliases_for_key("DATABASE_URL", af) == []


def test_set_alias_empty_key_raises(af):
    with pytest.raises(ValueError):
        set_alias("", "alias", af)


def test_set_alias_empty_alias_raises(af):
    with pytest.raises(ValueError):
        set_alias("KEY", "", af)
