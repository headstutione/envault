"""Tests for envault.labels module."""
import pytest
from pathlib import Path
from envault.labels import (
    add_label, remove_label, get_labels, list_labels, find_by_label
)


@pytest.fixture
def lf(tmp_path) -> Path:
    return tmp_path / "labels.json"


def test_get_labels_returns_empty_when_missing(lf):
    assert get_labels("MY_KEY", lf) == []


def test_add_label_creates_entry(lf):
    add_label("MY_KEY", "production", lf)
    assert "production" in get_labels("MY_KEY", lf)


def test_add_label_no_duplicates(lf):
    add_label("MY_KEY", "production", lf)
    add_label("MY_KEY", "production", lf)
    assert get_labels("MY_KEY", lf).count("production") == 1


def test_add_multiple_labels(lf):
    add_label("MY_KEY", "production", lf)
    add_label("MY_KEY", "critical", lf)
    labels = get_labels("MY_KEY", lf)
    assert "production" in labels
    assert "critical" in labels


def test_remove_label_returns_true(lf):
    add_label("MY_KEY", "staging", lf)
    result = remove_label("MY_KEY", "staging", lf)
    assert result is True
    assert "staging" not in get_labels("MY_KEY", lf)


def test_remove_label_returns_false_when_missing(lf):
    result = remove_label("MY_KEY", "nonexistent", lf)
    assert result is False


def test_remove_last_label_clears_key(lf):
    add_label("MY_KEY", "solo", lf)
    remove_label("MY_KEY", "solo", lf)
    assert "MY_KEY" not in list_labels(lf)


def test_list_labels_returns_all(lf):
    add_label("KEY_A", "alpha", lf)
    add_label("KEY_B", "beta", lf)
    all_labels = list_labels(lf)
    assert "KEY_A" in all_labels
    assert "KEY_B" in all_labels


def test_find_by_label_returns_matching_keys(lf):
    add_label("KEY_A", "shared", lf)
    add_label("KEY_B", "shared", lf)
    add_label("KEY_C", "other", lf)
    keys = find_by_label("shared", lf)
    assert "KEY_A" in keys
    assert "KEY_B" in keys
    assert "KEY_C" not in keys


def test_add_empty_label_raises(lf):
    with pytest.raises(ValueError, match="empty"):
        add_label("MY_KEY", "  ", lf)
