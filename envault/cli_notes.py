"""CLI commands for per-key notes."""

import click
from envault.notes import set_note, get_note, remove_note, list_notes


@click.group()
def notes():
    """Manage notes attached to vault keys."""
    pass


@notes.command("set")
@click.argument("key")
@click.argument("note")
@click.option("--notes-file", default=".envault_notes.json", show_default=True)
def set_cmd(key, note, notes_file):
    """Attach NOTE to KEY."""
    try:
        set_note(key, note, notes_file)
        click.echo(f"Note set for '{key}'.")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@notes.command("get")
@click.argument("key")
@click.option("--notes-file", default=".envault_notes.json", show_default=True)
def get_cmd(key, notes_file):
    """Show the note for KEY."""
    note = get_note(key, notes_file)
    if note is None:
        click.echo(f"No note found for '{key}'.")
    else:
        click.echo(note)


@notes.command("remove")
@click.argument("key")
@click.option("--notes-file", default=".envault_notes.json", show_default=True)
def remove_cmd(key, notes_file):
    """Remove the note for KEY."""
    removed = remove_note(key, notes_file)
    if removed:
        click.echo(f"Note removed for '{key}'.")
    else:
        click.echo(f"No note found for '{key}'.")


@notes.command("list")
@click.option("--notes-file", default=".envault_notes.json", show_default=True)
def list_cmd(notes_file):
    """List all notes."""
    data = list_notes(notes_file)
    if not data:
        click.echo("No notes stored.")
        return
    for key, note in sorted(data.items()):
        click.echo(f"{key}: {note}")
