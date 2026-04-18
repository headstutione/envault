"""CLI commands for vault backup management."""
from __future__ import annotations

from pathlib import Path

import click

from envault.backup import create_backup, list_backups, restore_backup, prune_backups

DEFAULT_VAULT = Path(".envault.json")
DEFAULT_BACKUP_DIR = Path(".envault_backups")


@click.group()
def backup() -> None:
    """Manage vault backups."""


@backup.command("create")
@click.option("--vault", default=str(DEFAULT_VAULT), show_default=True)
@click.option("--backup-dir", default=str(DEFAULT_BACKUP_DIR), show_default=True)
def create_cmd(vault: str, backup_dir: str) -> None:
    """Create a snapshot of the current vault."""
    try:
        dest = create_backup(Path(vault), Path(backup_dir))
        click.echo(f"Backup created: {dest}")
    except FileNotFoundError as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1)


@backup.command("list")
@click.option("--backup-dir", default=str(DEFAULT_BACKUP_DIR), show_default=True)
def list_cmd(backup_dir: str) -> None:
    """List available backups."""
    backups = list_backups(Path(backup_dir))
    if not backups:
        click.echo("No backups found.")
    for p in backups:
        click.echo(p.name)


@backup.command("restore")
@click.argument("backup_file")
@click.option("--vault", default=str(DEFAULT_VAULT), show_default=True)
def restore_cmd(backup_file: str, vault: str) -> None:
    """Restore vault from a backup snapshot."""
    try:
        restore_backup(Path(backup_file), Path(vault))
        click.echo(f"Vault restored from {backup_file}")
    except FileNotFoundError as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1)


@backup.command("prune")
@click.option("--keep", default=5, show_default=True, help="Number of backups to keep.")
@click.option("--backup-dir", default=str(DEFAULT_BACKUP_DIR), show_default=True)
def prune_cmd(keep: int, backup_dir: str) -> None:
    """Remove oldest backups, keeping the N most recent."""
    removed = prune_backups(Path(backup_dir), keep=keep)
    if removed:
        for p in removed:
            click.echo(f"Removed: {p.name}")
    else:
        click.echo("Nothing to prune.")
