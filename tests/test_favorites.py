"""Tests for envault.favorites and cli_favorites."""
import pytest
from click.testing import CliRunner
from envault.favorites import (
    add_favorite, remove_favorite, list_favorites,
    is_favorite, clear_favorites,
)
from envault.cli_favorites import favorites


@pytest.fixture
def ff(tmp_path):
    return str(tmp_path / "favorites.json")


@pytest.fixture
def runner():
    return CliRunner()


def test_list_favorites_empty_when_missing(ff):
    assert list_favorites(ff) == []


def test_add_favorite_creates_entry(ff):
    add_favorite("DB_URL", ff)
    assert "DB_URL" in list_favorites(ff)


def test_add_favorite_no_duplicates(ff):
    add_favorite("DB_URL", ff)
    with pytest.raises(ValueError, match="already a favorite"):
        add_favorite("DB_URL", ff)


def test_add_multiple_favorites(ff):
    add_favorite("KEY_A", ff)
    add_favorite("KEY_B", ff)
    favs = list_favorites(ff)
    assert "KEY_A" in favs
    assert "KEY_B" in favs


def test_remove_favorite(ff):
    add_favorite("DB_URL", ff)
    remove_favorite("DB_URL", ff)
    assert "DB_URL" not in list_favorites(ff)


def test_remove_missing_raises(ff):
    with pytest.raises(KeyError):
        remove_favorite("MISSING", ff)


def test_is_favorite_true(ff):
    add_favorite("SECRET", ff)
    assert is_favorite("SECRET", ff) is True


def test_is_favorite_false(ff):
    assert is_favorite("NOPE", ff) is False


def test_clear_favorites(ff):
    add_favorite("A", ff)
    add_favorite("B", ff)
    clear_favorites(ff)
    assert list_favorites(ff) == []


def test_cli_add_and_list(runner, ff):
    result = runner.invoke(favorites, ["add", "API_KEY", "--file", ff])
    assert result.exit_code == 0
    assert "Added" in result.output
    result = runner.invoke(favorites, ["list", "--file", ff])
    assert "API_KEY" in result.output


def test_cli_add_duplicate_shows_error(runner, ff):
    runner.invoke(favorites, ["add", "API_KEY", "--file", ff])
    result = runner.invoke(favorites, ["add", "API_KEY", "--file", ff])
    assert "Error" in result.output


def test_cli_remove_command(runner, ff):
    runner.invoke(favorites, ["add", "API_KEY", "--file", ff])
    result = runner.invoke(favorites, ["remove", "API_KEY", "--file", ff])
    assert result.exit_code == 0
    assert "Removed" in result.output


def test_cli_list_empty(runner, ff):
    result = runner.invoke(favorites, ["list", "--file", ff])
    assert "No favorites" in result.output


def test_cli_clear_command(runner, ff):
    runner.invoke(favorites, ["add", "X", "--file", ff])
    result = runner.invoke(favorites, ["clear", "--file", ff])
    assert result.exit_code == 0
    assert "cleared" in result.output
