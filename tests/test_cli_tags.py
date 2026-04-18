"""Tests for envault/cli_tags.py"""
import pytest
from click.testing import CliRunner
from pathlib import Path
from envault.cli_tags import tags


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def tf(tmp_path):
    return str(tmp_path / "tags.json")


def test_add_and_list_tag(runner, tf):
    runner.invoke(tags, ["add", "DB_URL", "database", "--tags-file", tf])
    result = runner.invoke(tags, ["list", "DB_URL", "--tags-file", tf])
    assert "database" in result.output


def test_list_no_tags(runner, tf):
    result = runner.invoke(tags, ["list", "MISSING", "--tags-file", tf])
    assert "No tags" in result.output


def test_remove_tag(runner, tf):
    runner.invoke(tags, ["add", "DB_URL", "database", "--tags-file", tf])
    runner.invoke(tags, ["remove", "DB_URL", "database", "--tags-file", tf])
    result = runner.invoke(tags, ["list", "DB_URL", "--tags-file", tf])
    assert "No tags" in result.output


def test_find_by_tag(runner, tf):
    runner.invoke(tags, ["add", "DB_URL", "prod", "--tags-file", tf])
    runner.invoke(tags, ["add", "API_KEY", "prod", "--tags-file", tf])
    result = runner.invoke(tags, ["find", "prod", "--tags-file", tf])
    assert "DB_URL" in result.output
    assert "API_KEY" in result.output


def test_find_no_match(runner, tf):
    result = runner.invoke(tags, ["find", "ghost", "--tags-file", tf])
    assert "No variables" in result.output


def test_clear_tags(runner, tf):
    runner.invoke(tags, ["add", "DB_URL", "a", "--tags-file", tf])
    runner.invoke(tags, ["clear", "DB_URL", "--tags-file", tf])
    result = runner.invoke(tags, ["list", "DB_URL", "--tags-file", tf])
    assert "No tags" in result.output


def test_all_shows_entries(runner, tf):
    runner.invoke(tags, ["add", "K1", "t1", "--tags-file", tf])
    result = runner.invoke(tags, ["all", "--tags-file", tf])
    assert "K1" in result.output
    assert "t1" in result.output


def test_all_empty(runner, tf):
    result = runner.invoke(tags, ["all", "--tags-file", tf])
    assert "No tags defined" in result.output
