"""CLI commands for managing key groups."""
import click
from envault.groups import (
    create_group, delete_group, add_key_to_group,
    remove_key_from_group, get_group_keys, list_groups
)


@click.group("groups")
def groups():
    """Manage key groups."""


@groups.command("create")
@click.argument("name")
@click.argument("keys", nargs=-1, required=True)
@click.option("--file", "gf", default=".envault_groups.json")
def create_cmd(name, keys, gf):
    """Create a new group with the given keys."""
    try:
        create_group(name, list(keys), gf)
        click.echo(f"Group '{name}' created with {len(keys)} key(s).")
    except (ValueError, KeyError) as e:
        click.echo(f"Error: {e}", err=True)


@groups.command("delete")
@click.argument("name")
@click.option("--file", "gf", default=".envault_groups.json")
def delete_cmd(name, gf):
    """Delete a group."""
    try:
        delete_group(name, gf)
        click.echo(f"Group '{name}' deleted.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)


@groups.command("add-key")
@click.argument("name")
@click.argument("key")
@click.option("--file", "gf", default=".envault_groups.json")
def add_key_cmd(name, key, gf):
    """Add a key to an existing group."""
    try:
        add_key_to_group(name, key, gf)
        click.echo(f"Key '{key}' added to group '{name}'.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)


@groups.command("remove-key")
@click.argument("name")
@click.argument("key")
@click.option("--file", "gf", default=".envault_groups.json")
def remove_key_cmd(name, key, gf):
    """Remove a key from a group."""
    try:
        remove_key_from_group(name, key, gf)
        click.echo(f"Key '{key}' removed from group '{name}'.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)


@groups.command("list")
@click.option("--file", "gf", default=".envault_groups.json")
def list_cmd(gf):
    """List all groups."""
    names = list_groups(gf)
    if not names:
        click.echo("No groups defined.")
    else:
        for n in names:
            click.echo(n)


@groups.command("show")
@click.argument("name")
@click.option("--file", "gf", default=".envault_groups.json")
def show_cmd(name, gf):
    """Show keys in a group."""
    try:
        keys = get_group_keys(name, gf)
        if not keys:
            click.echo(f"Group '{name}' is empty.")
        else:
            for k in keys:
                click.echo(k)
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)
