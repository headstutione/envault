import click
from envault.history import get_history, clear_history


@click.group()
def history():
    """View and manage variable change history."""
    pass


@history.command("log")
@click.argument("key")
@click.option("--history-file", default=".envault_history.json", show_default=True)
def log_cmd(key, history_file):
    """Show change history for a variable KEY."""
    entries = get_history(key, history_file=history_file)
    if not entries:
        click.echo(f"No history found for '{key}'.")
        return
    for entry in entries:
        click.echo(f"[{entry['timestamp']}] {entry['action']} by {entry.get('user', 'unknown')}")


@history.command("clear")
@click.argument("key")
@click.option("--history-file", default=".envault_history.json", show_default=True)
@click.confirmation_option(prompt=f"Clear history for key?")
def clear_cmd(key, history_file):
    """Clear change history for a variable KEY."""
    clear_history(key, history_file=history_file)
    click.echo(f"History cleared for '{key}'.")


@history.command("list-keys")
@click.option("--history-file", default=".envault_history.json", show_default=True)
def list_keys_cmd(history_file):
    """List all keys that have recorded history."""
    from envault.history import _load_history
    data = _load_history(history_file)
    if not data:
        click.echo("No history recorded.")
        return
    for key in sorted(data.keys()):
        count = len(data[key])
        click.echo(f"{key}  ({count} entries)")
