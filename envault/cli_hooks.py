"""CLI commands for managing hooks."""
import click
from pathlib import Path
from envault.hooks import set_hook, remove_hook, list_hooks, get_hook

DEFAULT_HOOKS_FILE = Path(".envault_hooks.json")


@click.group()
def hooks():
    """Manage pre/post operation hooks."""


@hooks.command("set")
@click.argument("event")
@click.argument("command")
@click.option("--hooks-file", default=str(DEFAULT_HOOKS_FILE), show_default=True)
def set_cmd(event, command, hooks_file):
    """Register COMMAND to run on EVENT."""
    try:
        set_hook(event, command, Path(hooks_file))
        click.echo(f"Hook set: {event} -> {command}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@hooks.command("remove")
@click.argument("event")
@click.option("--hooks-file", default=str(DEFAULT_HOOKS_FILE), show_default=True)
def remove_cmd(event, hooks_file):
    """Remove the hook for EVENT."""
    removed = remove_hook(event, Path(hooks_file))
    if removed:
        click.echo(f"Hook removed: {event}")
    else:
        click.echo(f"No hook found for event '{event}'.")


@hooks.command("list")
@click.option("--hooks-file", default=str(DEFAULT_HOOKS_FILE), show_default=True)
def list_cmd(hooks_file):
    """List all registered hooks."""
    entries = list_hooks(Path(hooks_file))
    if not entries:
        click.echo("No hooks registered.")
        return
    for entry in entries:
        click.echo(f"{entry['event']}: {entry['command']}")


@hooks.command("get")
@click.argument("event")
@click.option("--hooks-file", default=str(DEFAULT_HOOKS_FILE), show_default=True)
def get_cmd(event, hooks_file):
    """Show the hook command for EVENT."""
    cmd = get_hook(event, Path(hooks_file))
    if cmd is None:
        click.echo(f"No hook for '{event}'.")
    else:
        click.echo(cmd)
