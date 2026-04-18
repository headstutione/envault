import json
import pytest
from click.testing import CliRunner
from pathlib import Path
from envault.vault import set_variable
from envault.lint import lint_vault, LintIssue
from envault.cli_lint import lint

@pytest.fixture
def vault_file(tmp_path):
    return str(tmp_path / 'vault.json')

PASSWORD = 'testpass'

def test_lint_clean_vault(vault_file):
    set_variable(vault_file, 'DB_HOST', 'localhost', PASSWORD)
    set_variable(vault_file, 'API_KEY', 'secret123', PASSWORD)
    issues = lint_vault(vault_file, PASSWORD)
    assert issues == []

def test_lint_bad_key_name(vault_file):
    set_variable(vault_file, 'bad-key', 'value', PASSWORD)
    issues = lint_vault(vault_file, PASSWORD)
    warnings = [i for i in issues if i.level == 'warning']
    assert any('bad-key' in i.key for i in warnings)

def test_lint_empty_value(vault_file):
    set_variable(vault_file, 'EMPTY_VAR', '   ', PASSWORD)
    issues = lint_vault(vault_file, PASSWORD)
    assert any(i.key == 'EMPTY_VAR' and i.level == 'warning' for i in issues)

def test_lint_empty_vault(vault_file):
    issues = lint_vault(vault_file, PASSWORD)
    assert issues == []

def test_lint_wrong_password(vault_file):
    set_variable(vault_file, 'SOME_KEY', 'value', PASSWORD)
    issues = lint_vault(vault_file, 'wrongpass')
    assert any(i.level == 'error' for i in issues)

def test_lint_multiple_issues(vault_file):
    """Multiple keys with issues should each produce their own warning."""
    set_variable(vault_file, 'bad-key', 'value', PASSWORD)
    set_variable(vault_file, 'another.bad', '   ', PASSWORD)
    issues = lint_vault(vault_file, PASSWORD)
    warned_keys = {i.key for i in issues if i.level == 'warning'}
    assert 'bad-key' in warned_keys
    assert 'another.bad' in warned_keys

def test_cli_lint_no_issues(vault_file):
    set_variable(vault_file, 'GOOD_KEY', 'goodvalue', PASSWORD)
    runner = CliRunner()
    result = runner.invoke(lint, ['run', '--vault', vault_file, '--password', PASSWORD])
    assert result.exit_code == 0
    assert 'No issues found' in result.output

def test_cli_lint_shows_warnings(vault_file):
    set_variable(vault_file, 'bad.key', 'value', PASSWORD)
    runner = CliRunner()
    result = runner.invoke(lint, ['run', '--vault', vault_file, '--password', PASSWORD])
    assert '[WARN]' in result.output

def test_cli_lint_error_exits_nonzero(vault_file):
    set_variable(vault_file, 'SOME_KEY', 'value', PASSWORD)
    runner = CliRunner()
    result = runner.invoke(lint, ['run', '--vault', vault_file, '--password', 'wrong'])
    assert result.exit_code != 0
