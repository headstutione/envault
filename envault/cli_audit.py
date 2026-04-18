"""CLI commands for audit log."""

import click
from envault.audit import get_log, clear_log, DEFAULT_AUDIT_FILE


@click.group("audit")
def audit():
    """View and manage the audit log."""
    pass


@audit.command("log")
@click.option("--audit-file", default=DEFAULT_AUDIT_FILE, show_default=True)
@click.option("--key", default=None, help="Filter by key name.")
def log_cmd(audit_file, key):
    """Display audit log entries."""
    entries = get_log(audit_file)
    if key:
        entries = [e for e in entries if e["key"] == key]
    if not entries:
        click.echo("No audit log entries found.")
        return
    for entry in entries:
        click.echo(f"{entry['timestamp']}  {entry['action']:10s}  {entry['key']}")


@audit.command("clear")
@click.option("--audit-file", default=DEFAULT_AUDIT_FILE, show_default=True)
@click.confirmation_option(prompt="Are you sure you want to clear the audit log?")
def clear_cmd(audit_file):
    """Clear all audit log entries."""
    clear_log(audit_file)
    click.echo("Audit log cleared.")
