import click
from pathlib import Path
from envault.snapshots import create_snapshot, list_snapshots, restore_snapshot, delete_snapshot


@click.group()
def snapshots():
    """Manage vault snapshots."""
    pass


@snapshots.command("create")
@click.option("--vault", default=".envault/vault.enc", show_default=True)
@click.option("--label", default=None, help="Optional label for the snapshot.")
def create_cmd(vault, label):
    """Create a snapshot of the current vault."""
    try:
        path = create_snapshot(vault_path=vault, label=label)
        click.echo(f"Snapshot created: {path}")
    except FileNotFoundError:
        click.echo("Error: vault file not found.", err=True)


@snapshots.command("list")
@click.option("--vault", default=".envault/vault.enc", show_default=True)
def list_cmd(vault):
    """List all snapshots for the vault."""
    entries = list_snapshots(vault_path=vault)
    if not entries:
        click.echo("No snapshots found.")
        return
    for entry in entries:
        label = f"  [{entry['label']}]" if entry.get("label") else ""
        click.echo(f"{entry['id']}  {entry['created_at']}{label}")


@snapshots.command("restore")
@click.argument("snapshot_id")
@click.option("--vault", default=".envault/vault.enc", show_default=True)
def restore_cmd(snapshot_id, vault):
    """Restore vault from a snapshot."""
    try:
        restore_snapshot(snapshot_id=snapshot_id, vault_path=vault)
        click.echo(f"Vault restored from snapshot {snapshot_id}.")
    except KeyError:
        click.echo(f"Error: snapshot '{snapshot_id}' not found.", err=True)


@snapshots.command("delete")
@click.argument("snapshot_id")
@click.option("--vault", default=".envault/vault.enc", show_default=True)
def delete_cmd(snapshot_id, vault):
    """Delete a snapshot."""
    try:
        delete_snapshot(snapshot_id=snapshot_id, vault_path=vault)
        click.echo(f"Snapshot {snapshot_id} deleted.")
    except KeyError:
        click.echo(f"Error: snapshot '{snapshot_id}' not found.", err=True)
