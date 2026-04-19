"""CLI commands for managing favorite vault keys."""
import click
from envault.favorites import (
    add_favorite,
    remove_favorite,
    list_favorites,
    is_favorite,
    clear_favorites,
    DEFAULT_FAVORITES_FILE,
)


@click.group()
def favorites():
    """Manage pinned/favorite vault keys."""


@favorites.command("add")
@click.argument("key")
@click.option("--file", "ffile", default=DEFAULT_FAVORITES_FILE, show_default=True)
def add_cmd(key: str, ffile: str):
    """Pin a key as a favorite."""
    try:
        add_favorite(key, ffile)
        click.echo(f"Added '{key}' to favorites.")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@favorites.command("remove")
@click.argument("key")
@click.option("--file", "ffile", default=DEFAULT_FAVORITES_FILE, show_default=True)
def remove_cmd(key: str, ffile: str):
    """Unpin a favorite key."""
    try:
        remove_favorite(key, ffile)
        click.echo(f"Removed '{key}' from favorites.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)


@favorites.command("list")
@click.option("--file", "ffile", default=DEFAULT_FAVORITES_FILE, show_default=True)
def list_cmd(ffile: str):
    """List all favorite keys."""
    favs = list_favorites(ffile)
    if not favs:
        click.echo("No favorites set.")
    else:
        for key in favs:
            click.echo(key)


@favorites.command("check")
@click.argument("key")
@click.option("--file", "ffile", default=DEFAULT_FAVORITES_FILE, show_default=True)
def check_cmd(key: str, ffile: str):
    """Check if a key is a favorite."""
    if is_favorite(key, ffile):
        click.echo(f"'{key}' is a favorite.")
    else:
        click.echo(f"'{key}' is not a favorite.")


@favorites.command("clear")
@click.option("--file", "ffile", default=DEFAULT_FAVORITES_FILE, show_default=True)
def clear_cmd(ffile: str):
    """Clear all favorites."""
    clear_favorites(ffile)
    click.echo("All favorites cleared.")
