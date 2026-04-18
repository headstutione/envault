"""CLI commands for managing variable TTL/expiry."""
import click
from pathlib import Path
import time
from envault.ttl import (
    set_expiry, get_expiry, remove_expiry, list_expiries, purge_expired, is_expired
)

TTL_FILE = Path(".envault_ttl.json")


@click.group()
def ttl():
    """Manage variable expiry (TTL)."""


@ttl.command("set")
@click.argument("key")
@click.argument("seconds", type=int)
def set_cmd(key, seconds):
    """Set TTL for KEY to SECONDS seconds from now."""
    try:
        expires_at = set_expiry(key, seconds, TTL_FILE)
        human = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expires_at))
        click.echo(f"Expiry set for '{key}': {human}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@ttl.command("get")
@click.argument("key")
def get_cmd(key):
    """Show expiry time for KEY."""
    expiry = get_expiry(key, TTL_FILE)
    if expiry is None:
        click.echo(f"No TTL set for '{key}'.")
    else:
        human = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expiry))
        expired = " (EXPIRED)" if time.time() > expiry else ""
        click.echo(f"{key}: {human}{expired}")


@ttl.command("remove")
@click.argument("key")
def remove_cmd(key):
    """Remove TTL for KEY."""
    if remove_expiry(key, TTL_FILE):
        click.echo(f"TTL removed for '{key}'.")
    else:
        click.echo(f"No TTL found for '{key}'.")


@ttl.command("list")
def list_cmd():
    """List all keys with expiry times."""
    data = list_expiries(TTL_FILE)
    if not data:
        click.echo("No TTL entries found.")
        return
    now = time.time()
    for key, expiry in sorted(data.items()):
        human = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expiry))
        status = " [EXPIRED]" if now > expiry else ""
        click.echo(f"{key}: {human}{status}")


@ttl.command("purge")
def purge_cmd():
    """Remove all expired TTL entries."""
    purged = purge_expired(TTL_FILE)
    if purged:
        click.echo(f"Purged {len(purged)} expired entries: {', '.join(purged)}")
    else:
        click.echo("No expired entries to purge.")
