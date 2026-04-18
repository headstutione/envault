"""CLI commands for team sharing (export / import bundles)."""

import click
from pathlib import Path

from envault.sharing import export_bundle, import_bundle

DEFAULT_VAULT = Path(".envault")


@click.group()
def sharing():
    """Commands for sharing vault bundles with teammates."""


@sharing.command("export")
@click.argument("output", type=click.Path())
@click.password_option("--password", "-p", help="Vault password")
@click.option("--vault", default=str(DEFAULT_VAULT), show_default=True, help="Vault file path")
def export_cmd(output: str, password: str, vault: str) -> None:
    """Export vault to an encrypted shareable bundle."""
    vault_path = Path(vault)
    if not vault_path.exists():
        raise click.ClickException(f"Vault not found: {vault}")
    try:
        export_bundle(vault_path, password, Path(output))
        click.echo(f"Bundle exported to {output}")
    except ValueError as exc:
        raise click.ClickException(str(exc))


@sharing.command("import")
@click.argument("bundle", type=click.Path(exists=True))
@click.password_option("--password", "-p", help="Bundle password")
@click.option("--vault", default=str(DEFAULT_VAULT), show_default=True, help="Vault file path")
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing keys with values from bundle",
)
def import_cmd(bundle: str, password: str, vault: str, overwrite: bool) -> None:
    """Import an encrypted bundle into the local vault."""
    try:
        result = import_bundle(Path(bundle), password, Path(vault), overwrite=overwrite)
    except ValueError as exc:
        raise click.ClickException(str(exc))

    if result["added"]:
        click.echo("Added: " + ", ".join(result["added"]))
    if result["skipped"]:
        click.echo(
            "Skipped (already exist, use --overwrite to replace): "
            + ", ".join(result["skipped"])
        )
    if not result["added"] and not result["skipped"]:
        click.echo("Nothing imported.")
