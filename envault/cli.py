"""Main CLI entry point for envault."""
import click
from pathlib import Path
from envault.vault import set_variable, get_variable, delete_variable, list_variables
from envault.cli_sharing import sharing
from envault.cli_audit import audit
from envault.cli_rotation import rotation
from envault.cli_search import search
from envault.cli_backup import backup
from envault.cli_tags import tags

DEFAULT_VAULT = Path(".envault")


@click.group()
def cli():
    """envault — encrypted environment variable manager."""


@cli.command("set")
@click.argument("key")
@click.argument("value")
@click.password_option("--password", prompt="Vault password")
@click.option("--vault-file", default=str(DEFAULT_VAULT), show_default=True)
def set_cmd(key, value, password, vault_file):
    """Set an environment variable."""
    set_variable(key, value, password, Path(vault_file))
    click.echo(f"Set '{key}'.")


@cli.command("get")
@click.argument("key")
@click.option("--password", prompt="Vault password", hide_input=True)
@click.option("--vault-file", default=str(DEFAULT_VAULT), show_default=True)
def get_cmd(key, password, vault_file):
    """Get an environment variable."""
    value = get_variable(key, password, Path(vault_file))
    if value is None:
        click.echo(f"Key '{key}' not found.")
    else:
        click.echo(value)


@cli.command("delete")
@click.argument("key")
@click.option("--password", prompt="Vault password", hide_input=True)
@click.option("--vault-file", default=str(DEFAULT_VAULT), show_default=True)
def delete_cmd(key, password, vault_file):
    """Delete an environment variable."""
    deleted = delete_variable(key, password, Path(vault_file))
    if deleted:
        click.echo(f"Deleted '{key}'.")
    else:
        click.echo(f"Key '{key}' not found.")


@cli.command("list")
@click.option("--password", prompt="Vault password", hide_input=True)
@click.option("--vault-file", default=str(DEFAULT_VAULT), show_default=True)
def list_cmd(password, vault_file):
    """List all variable keys."""
    keys = list_variables(password, Path(vault_file))
    if keys:
        for k in keys:
            click.echo(k)
    else:
        click.echo("No variables stored.")


cli.add_command(sharing)
cli.add_command(audit)
cli.add_command(rotation)
cli.add_command(search)
cli.add_command(backup)
cli.add_command(tags)

if __name__ == "__main__":
    cli()
