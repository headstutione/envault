import json
import pytest
from click.testing import CliRunner
from envault.cli_templates import templates
from envault.vault import save_vault, set_variable


@pytest.fixture
def runner():
    return CliRunner()


def test_create_and_list_template(runner, tmp_path):
    tf = str(tmp_path / "templates.json")
    result = runner.invoke(templates, ["create", "web", "DB_URL", "SECRET_KEY", "--file", tf])
    assert result.exit_code == 0
    assert "web" in result.output

    result = runner.invoke(templates, ["list", "--file", tf])
    assert result.exit_code == 0
    assert "web" in result.output
    assert "DB_URL" in result.output


def test_create_duplicate_shows_error(runner, tmp_path):
    tf = str(tmp_path / "templates.json")
    runner.invoke(templates, ["create", "web", "DB_URL", "--file", tf])
    result = runner.invoke(templates, ["create", "web", "OTHER", "--file", tf])
    assert result.exit_code == 0
    assert "Error" in result.output


def test_delete_template(runner, tmp_path):
    tf = str(tmp_path / "templates.json")
    runner.invoke(templates, ["create", "web", "DB_URL", "--file", tf])
    result = runner.invoke(templates, ["delete", "web", "--file", tf])
    assert result.exit_code == 0
    assert "deleted" in result.output

    result = runner.invoke(templates, ["list", "--file", tf])
    assert "No templates" in result.output


def test_delete_missing_template_shows_error(runner, tmp_path):
    tf = str(tmp_path / "templates.json")
    result = runner.invoke(templates, ["delete", "ghost", "--file", tf])
    assert "Error" in result.output


def test_apply_all_keys_present(runner, tmp_path):
    tf = str(tmp_path / "templates.json")
    vf = str(tmp_path / "vault.json")
    password = "secret"
    runner.invoke(templates, ["create", "web", "DB_URL", "--file", tf])
    set_variable("DB_URL", "postgres://localhost", password, vault_file=vf)
    result = runner.invoke(templates, ["apply", "web", "--vault", vf, "--file", tf, "--password", password])
    assert result.exit_code == 0
    assert "present" in result.output


def test_apply_missing_keys(runner, tmp_path):
    tf = str(tmp_path / "templates.json")
    vf = str(tmp_path / "vault.json")
    password = "secret"
    runner.invoke(templates, ["create", "web", "DB_URL", "SECRET_KEY", "--file", tf])
    set_variable("DB_URL", "postgres://localhost", password, vault_file=vf)
    result = runner.invoke(templates, ["apply", "web", "--vault", vf, "--file", tf, "--password", password])
    assert "Missing" in result.output
    assert "SECRET_KEY" in result.output
