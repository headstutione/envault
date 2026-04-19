"""CLI commands for managing variable reminders."""

import click
from pathlib import Path
from datetime import datetime, timezone, timedelta
from envault.reminders import set_reminder, remove_reminder, get_reminder, list_reminders, due_reminders

REMINDERS_FILE = Path(".envault_reminders.json")


@click.group()
def reminders():
    """Manage reminders for environment variables."""


@reminders.command("set")
@click.argument("key")
@click.option("--days", type=int, default=None, help="Remind in N days from now.")
@click.option("--at", "remind_at", default=None, help="ISO datetime to remind at.")
@click.option("--note", default="", help="Optional reminder note.")
def set_cmd(key, days, remind_at, note):
    """Set a reminder for KEY."""
    if days is not None:
        dt = datetime.now(timezone.utc) + timedelta(days=days)
    elif remind_at:
        try:
            dt = datetime.fromisoformat(remind_at)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        except ValueError:
            click.echo(f"Error: invalid datetime '{remind_at}'.")
            return
    else:
        click.echo("Error: provide --days or --at.")
        return
    set_reminder(key, dt, note=note, reminders_file=REMINDERS_FILE)
    click.echo(f"Reminder set for '{key}' at {dt.isoformat()}.")


@reminders.command("remove")
@click.argument("key")
def remove_cmd(key):
    """Remove reminder for KEY."""
    remove_reminder(key, reminders_file=REMINDERS_FILE)
    click.echo(f"Reminder for '{key}' removed.")


@reminders.command("list")
def list_cmd():
    """List all reminders."""
    data = list_reminders(reminders_file=REMINDERS_FILE)
    if not data:
        click.echo("No reminders set.")
        return
    for key, entry in data.items():
        note = f" — {entry['note']}" if entry.get("note") else ""
        click.echo(f"{key}: {entry['remind_at']}{note}")


@reminders.command("due")
def due_cmd():
    """Show reminders that are currently due."""
    items = due_reminders(reminders_file=REMINDERS_FILE)
    if not items:
        click.echo("No reminders due.")
        return
    for key, entry in items:
        note = f" — {entry['note']}" if entry.get("note") else ""
        click.echo(f"DUE: {key} (was {entry['remind_at']}){note}")
