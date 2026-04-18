"""CLI commands for vault linting."""
import click
from envault.lint import lint_vault

@click.group()
def lint():
    """Lint vault keys and values."""

@lint.command('run')
@click.option('--vault', default='.envault/vault.json', show_default=True)
@click.option('--password', prompt=True, hide_input=True)
@click.option('--level', type=click.Choice(['all', 'error', 'warning']), default='all', show_default=True)
def run_cmd(vault, password, level):
    """Run lint checks on the vault."""
    try:
        issues = lint_vault(vault, password)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    filtered = [i for i in issues if level == 'all' or i.level == level]
    if not filtered:
        click.echo('No issues found.')
        return
    for issue in filtered:
        prefix = '[ERROR]' if issue.level == 'error' else '[WARN] '
        click.echo(f"{prefix} {issue.key}: {issue.message}")
    errors = sum(1 for i in filtered if i.level == 'error')
    if errors:
        raise SystemExit(1)
