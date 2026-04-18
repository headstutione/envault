import click
from pathlib import Path
from envault.vault import load_vault, save_vault, set_variable, get_variable, delete_variable, list_variables
from envault.cli_sharing import sharing

DEFAULT_VAULT = ".envault"


@click.group()
@click.option("--vault", default=DEFAULT_VAULT, show_default=True, help="Path to vault file.")
@click.pass_context
def cli(ctx, vault):
    """envault — manage and encrypt project environment variables."""
    ctx.ensure_object(dict)
    ctx.obj["vault"] = vault


@cli.command("set")
@click.argument("key")
@click.argument("value")
@click.password_option(prompt="Vault password", help="Password to encrypt the vault.")
@click.pass_context
def set_cmd(ctx, key, value, password):
    """Set an environment variable in the vault."""
    vault_path = ctx.obj["vault"]
    try:
        set_variable(vault_path, key, value, password)
        click.echo(f"Set '{key}' successfully.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@cli.command("get")
@click.argument("key")
@click.option("--password", prompt=True, hide_input=True, help="Vault password.")
@click.pass_context
def get_cmd(ctx, key, password):
    """Get an environment variable from the vault."""
    vault_path = ctx.obj["vault"]
    try:
        value = get_variable(vault_path, key, password)
        if value is None:
            click.echo(f"Key '{key}' not found.", err=True)
            raise SystemExit(1)
        click.echo(value)
    except SystemExit:
        raise
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@cli.command("delete")
@click.argument("key")
@click.option("--password", prompt=True, hide_input=True, help="Vault password.")
@click.pass_context
def delete_cmd(ctx, key, password):
    """Delete an environment variable from the vault."""
    vault_path = ctx.obj["vault"]
    try:
        delete_variable(vault_path, key, password)
        click.echo(f"Deleted '{key}'.")
    except KeyError:
        click.echo(f"Key '{key}' not found.", err=True)
        raise SystemExit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@cli.command("list")
@click.option("--password", prompt=True, hide_input=True, help="Vault password.")
@click.pass_context
def list_cmd(ctx, password):
    """List all keys in the vault."""
    vault_path = ctx.obj["vault"]
    try:
        keys = list_variables(vault_path, password)
        if not keys:
            click.echo("Vault is empty.")
        else:
            for key in keys:
                click.echo(key)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


cli.add_command(sharing, name="sharing")

if __name__ == "__main__":
    cli()
