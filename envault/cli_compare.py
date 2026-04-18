"""CLI commands for comparing vaults."""
import click
from pathlib import Path
from envault.compare import compare_vaults, compare_vault_dotenv

STATUS_SYMBOLS = {
    "match": ("=", "green"),
    "mismatch": ("~", "yellow"),
    "only_a": ("<", "cyan"),
    "only_b": (">", "magenta"),
}


@click.group()
def compare():
    """Compare vaults or vault vs .env file."""


@compare.command("vaults")
@click.argument("vault_a", type=click.Path(exists=True))
@click.argument("vault_b", type=click.Path(exists=True))
@click.option("--password-a", prompt="Password for vault A", hide_input=True)
@click.option("--password-b", prompt="Password for vault B", hide_input=True)
@click.option("--only-diff", is_flag=True, default=False, help="Hide matching keys")
def vaults_cmd(vault_a, vault_b, password_a, password_b, only_diff):
    """Compare two encrypted vault files."""
    try:
        results = compare_vaults(Path(vault_a), password_a, Path(vault_b), password_b)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    if not results:
        click.echo("Both vaults are empty.")
        return
    for r in results:
        if only_diff and r.status == "match":
            continue
        sym, color = STATUS_SYMBOLS[r.status]
        click.echo(click.style(f"[{sym}] {r.key}", fg=color))


@compare.command("dotenv")
@click.argument("vault", type=click.Path(exists=True))
@click.argument("dotenv", type=click.Path(exists=True))
@click.option("--password", prompt=True, hide_input=True)
@click.option("--only-diff", is_flag=True, default=False)
def dotenv_cmd(vault, dotenv, password, only_diff):
    """Compare an encrypted vault against a .env file."""
    try:
        results = compare_vault_dotenv(Path(vault), password, Path(dotenv))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    if not results:
        click.echo("Nothing to compare.")
        return
    for r in results:
        if only_diff and r.status == "match":
            continue
        sym, color = STATUS_SYMBOLS[r.status]
        click.echo(click.style(f"[{sym}] {r.key}", fg=color))
