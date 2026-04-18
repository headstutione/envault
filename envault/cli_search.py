import click
from envault.search import search_keys, search_values, list_keys
from envault.vault import load_vault


@click.group()
def search():
    """Search environment variable keys and values."""
    pass


@search.command("keys")
@click.argument("pattern")
@click.option("--vault", "vault_path", default=".envault", show_default=True)
@click.option("--password", prompt=True, hide_input=True)
def keys_cmd(pattern, vault_path, password):
    """Search keys matching a glob PATTERN."""
    try:
        vault = load_vault(vault_path, password)
    except FileNotFoundError:
        click.echo("Error: vault not found.", err=True)
        raise SystemExit(1)
    except ValueError:
        click.echo("Error: wrong password.", err=True)
        raise SystemExit(1)

    matches = search_keys(vault, pattern)
    if not matches:
        click.echo("No keys matched.")
    else:
        for key in matches:
            click.echo(key)


@search.command("values")
@click.argument("pattern")
@click.option("--vault", "vault_path", default=".envault", show_default=True)
@click.option("--password", prompt=True, hide_input=True)
def values_cmd(pattern, vault_path, password):
    """Search keys whose decrypted value matches a glob PATTERN."""
    try:
        vault = load_vault(vault_path, password)
    except FileNotFoundError:
        click.echo("Error: vault not found.", err=True)
        raise SystemExit(1)
    except ValueError:
        click.echo("Error: wrong password.", err=True)
        raise SystemExit(1)

    matches = search_values(vault, password, pattern)
    if not matches:
        click.echo("No values matched.")
    else:
        for key in matches:
            click.echo(key)


@search.command("list")
@click.option("--vault", "vault_path", default=".envault", show_default=True)
@click.option("--password", prompt=True, hide_input=True)
def list_cmd(vault_path, password):
    """List all keys in the vault."""
    try:
        vault = load_vault(vault_path, password)
    except FileNotFoundError:
        click.echo("Error: vault not found.", err=True)
        raise SystemExit(1)
    except ValueError:
        click.echo("Error: wrong password.", err=True)
        raise SystemExit(1)

    keys = list_keys(vault)
    if not keys:
        click.echo("Vault is empty.")
    else:
        for key in keys:
            click.echo(key)
