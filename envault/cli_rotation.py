"""CLI commands for key rotation in envault."""

from pathlib import Path

import click

from envault.rotation import rotate_password


@click.group()
def rotation():
    """Key rotation commands."""
    pass


@rotation.command("rotate")
@click.option("--vault", default=".envault.json", show_default=True, help="Vault file path.")
@click.option("--audit", default=None, help="Audit log file path.")
@click.password_option("--old-password", prompt="Old password", confirmation_prompt=False)
@click.password_option("--new-password", prompt="New password")
def rotate_cmd(vault, audit, old_password, new_password):
    """Re-encrypt all vault variables with a new password."""
    vault_path = Path(vault)
    audit_path = Path(audit) if audit else None

    if not vault_path.exists():
        click.echo("Error: vault file not found.", err=True)
        raise SystemExit(1)

    try:
        count = rotate_password(vault_path, old_password, new_password, audit_path)
        click.echo(f"Rotated {count} variable(s) to new password.")
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1)
