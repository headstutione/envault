"""CLI commands for profile management."""
import click
from pathlib import Path
from envault.profiles import (
    create_profile, delete_profile, assign_key,
    unassign_key, get_profile_keys, list_profiles,
    DEFAULT_PROFILES_FILE,
)


@click.group()
def profiles():
    """Manage variable profiles (e.g. dev, staging, prod)."""


@profiles.command("create")
@click.argument("name")
@click.option("--profiles-file", default=str(DEFAULT_PROFILES_FILE))
def create_cmd(name, profiles_file):
    """Create a new profile."""
    try:
        create_profile(name, Path(profiles_file))
        click.echo(f"Profile '{name}' created.")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@profiles.command("delete")
@click.argument("name")
@click.option("--profiles-file", default=str(DEFAULT_PROFILES_FILE))
def delete_cmd(name, profiles_file):
    """Delete a profile."""
    try:
        delete_profile(name, Path(profiles_file))
        click.echo(f"Profile '{name}' deleted.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)


@profiles.command("assign")
@click.argument("name")
@click.argument("key")
@click.option("--profiles-file", default=str(DEFAULT_PROFILES_FILE))
def assign_cmd(name, key, profiles_file):
    """Assign a variable key to a profile."""
    try:
        assign_key(name, key, Path(profiles_file))
        click.echo(f"Key '{key}' assigned to profile '{name}'.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)


@profiles.command("unassign")
@click.argument("name")
@click.argument("key")
@click.option("--profiles-file", default=str(DEFAULT_PROFILES_FILE))
def unassign_cmd(name, key, profiles_file):
    """Remove a variable key from a profile."""
    try:
        unassign_key(name, key, Path(profiles_file))
        click.echo(f"Key '{key}' removed from profile '{name}'.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)


@profiles.command("list")
@click.option("--profiles-file", default=str(DEFAULT_PROFILES_FILE))
def list_cmd(profiles_file):
    """List all profiles."""
    names = list_profiles(Path(profiles_file))
    if not names:
        click.echo("No profiles defined.")
    else:
        for n in names:
            click.echo(n)


@profiles.command("show")
@click.argument("name")
@click.option("--profiles-file", default=str(DEFAULT_PROFILES_FILE))
def show_cmd(name, profiles_file):
    """Show keys assigned to a profile."""
    try:
        keys = get_profile_keys(name, Path(profiles_file))
        if not keys:
            click.echo(f"Profile '{name}' has no keys assigned.")
        else:
            for k in keys:
                click.echo(k)
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)
