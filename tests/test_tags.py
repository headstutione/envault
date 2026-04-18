"""Tests for envault/tags.py"""
import pytest
from pathlib import Path
from envault.tags import add_tag, remove_tag, get_tags, keys_by_tag, clear_tags, all_tags


@pytest.fixture
def tags_file(tmp_path):
    return tmp_path / "tags.json"


def test_get_tags_returns_empty_when_missing(tags_file):
    assert get_tags("KEY", tags_file) == []


def test_add_tag_creates_entry(tags_file):
    add_tag("DB_URL", "database", tags_file)
    assert "database" in get_tags("DB_URL", tags_file)


def test_add_tag_no_duplicates(tags_file):
    add_tag("DB_URL", "database", tags_file)
    add_tag("DB_URL", "database", tags_file)
    assert get_tags("DB_URL", tags_file).count("database") == 1


def test_add_multiple_tags(tags_file):
    add_tag("API_KEY", "secret", tags_file)
    add_tag("API_KEY", "production", tags_file)
    result = get_tags("API_KEY", tags_file)
    assert "secret" in result
    assert "production" in result


def test_remove_tag(tags_file):
    add_tag("DB_URL", "database", tags_file)
    remove_tag("DB_URL", "database", tags_file)
    assert get_tags("DB_URL", tags_file) == []


def test_remove_tag_cleans_empty_key(tags_file):
    add_tag("DB_URL", "database", tags_file)
    remove_tag("DB_URL", "database", tags_file)
    assert "DB_URL" not in all_tags(tags_file)


def test_remove_nonexistent_tag_is_noop(tags_file):
    add_tag("DB_URL", "database", tags_file)
    remove_tag("DB_URL", "missing", tags_file)
    assert get_tags("DB_URL", tags_file) == ["database"]


def test_keys_by_tag_returns_matching(tags_file):
    add_tag("DB_URL", "production", tags_file)
    add_tag("API_KEY", "production", tags_file)
    add_tag("DEBUG", "dev", tags_file)
    result = keys_by_tag("production", tags_file)
    assert "DB_URL" in result
    assert "API_KEY" in result
    assert "DEBUG" not in result


def test_keys_by_tag_empty_when_none(tags_file):
    assert keys_by_tag("nonexistent", tags_file) == []


def test_clear_tags_removes_all(tags_file):
    add_tag("DB_URL", "a", tags_file)
    add_tag("DB_URL", "b", tags_file)
    clear_tags("DB_URL", tags_file)
    assert get_tags("DB_URL", tags_file) == []


def test_all_tags_returns_full_map(tags_file):
    add_tag("K1", "t1", tags_file)
    add_tag("K2", "t2", tags_file)
    data = all_tags(tags_file)
    assert "K1" in data
    assert "K2" in data
