import pytest
from click.testing import CliRunner
from unittest.mock import patch
from envault.cli_dependencies import dependencies

DEPS_MOD = "envault.cli_dependencies"


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def df(tmp_path):
    return str(tmp_path / "deps.json")


def _patch(df):
    return patch(f"{DEPS_MOD}.DEPS_FILE", df)


def test_add_command_succeeds(runner, df):
    with _patch(df):
        result = runner.invoke(dependencies, ["add", "KEY_A", "KEY_B"])
    assert result.exit_code == 0
    assert "KEY_A -> KEY_B" in result.output


def test_add_self_dependency_shows_error(runner, df):
    with _patch(df):
        result = runner.invoke(dependencies, ["add", "KEY_A", "KEY_A"])
    assert "Error" in result.output


def test_remove_command_succeeds(runner, df):
    with _patch(df):
        runner.invoke(dependencies, ["add", "KEY_A", "KEY_B"])
        result = runner.invoke(dependencies, ["remove", "KEY_A", "KEY_B"])
    assert result.exit_code == 0
    assert "Removed" in result.output


def test_remove_missing_shows_error(runner, df):
    with _patch(df):
        result = runner.invoke(dependencies, ["remove", "KEY_A", "KEY_B"])
    assert "Error" in result.output


def test_list_command_shows_deps(runner, df):
    with _patch(df):
        runner.invoke(dependencies, ["add", "KEY_A", "KEY_B"])
        result = runner.invoke(dependencies, ["list", "KEY_A"])
    assert "KEY_B" in result.output


def test_list_empty_shows_message(runner, df):
    with _patch(df):
        result = runner.invoke(dependencies, ["list", "KEY_A"])
    assert "No dependencies" in result.output


def test_dependents_command(runner, df):
    with _patch(df):
        runner.invoke(dependencies, ["add", "KEY_A", "KEY_B"])
        result = runner.invoke(dependencies, ["dependents", "KEY_B"])
    assert "KEY_A" in result.output


def test_all_command_shows_all(runner, df):
    with _patch(df):
        runner.invoke(dependencies, ["add", "KEY_A", "KEY_B"])
        runner.invoke(dependencies, ["add", "KEY_C", "KEY_D"])
        result = runner.invoke(dependencies, ["all"])
    assert "KEY_A" in result.output and "KEY_C" in result.output
