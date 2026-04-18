"""CLI commands for managing variable tags."""
import click
from pathlib import Path
from envault.tags import add_tag, remove_tag, get_tags, keys_by_tag, clear_tags, all_tags

DEFAULT_TAGS_FILE = Path(".envault_tags.json")


@click.group()
def tags():
    """Manage tags for vault variables."""


@tags.command("add")
@click.argument("key")
@click.argument("tag")
@click.option("--tags-file", default=str(DEFAULT_TAGS_FILE), show_default=True)
def add_cmd(key, tag, tags_file):
    """Add a tag to a variable."""
    add_tag(key, tag, Path(tags_file))
    click.echo(f"Tagged '{key}' with '{tag}'.")


@tags.command("remove")
@click.argument("key")
@click.argument("tag")
@click.option("--tags-file", default=str(DEFAULT_TAGS_FILE), show_default=True)
def remove_cmd(key, tag, tags_file):
    """Remove a tag from a variable."""
    remove_tag(key, tag, Path(tags_file))
    click.echo(f"Removed tag '{tag}' from '{key}'.")


@tags.command("list")
@click.argument("key")
@click.option("--tags-file", default=str(DEFAULT_TAGS_FILE), show_default=True)
def list_cmd(key, tags_file):
    """List tags for a variable."""
    result = get_tags(key, Path(tags_file))
    if result:
        click.echo(", ".join(result))
    else:
        click.echo(f"No tags for '{key}'.")


@tags.command("find")
@click.argument("tag")
@click.option("--tags-file", default=str(DEFAULT_TAGS_FILE), show_default=True)
def find_cmd(tag, tags_file):
    """Find all variables with a given tag."""
    keys = keys_by_tag(tag, Path(tags_file))
    if keys:
        for k in keys:
            click.echo(k)
    else:
        click.echo(f"No variables tagged '{tag}'.")


@tags.command("clear")
@click.argument("key")
@click.option("--tags-file", default=str(DEFAULT_TAGS_FILE), show_default=True)
def clear_cmd(key, tags_file):
    """Clear all tags from a variable."""
    clear_tags(key, Path(tags_file))
    click.echo(f"Cleared all tags from '{key}'.")


@tags.command("all")
@click.option("--tags-file", default=str(DEFAULT_TAGS_FILE), show_default=True)
def all_cmd(tags_file):
    """Show all tagged variables."""
    data = all_tags(Path(tags_file))
    if not data:
        click.echo("No tags defined.")
    else:
        for k, v in data.items():
            click.echo(f"{k}: {', '.join(v)}")
