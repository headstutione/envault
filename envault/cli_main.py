"""Main CLI entry point for envault."""
import click
from envault.cli import cli
from envault.cli_sharing import sharing
from envault.cli_audit import audit
from envault.cli_rotation import rotation
from envault.cli_search import search
from envault.cli_backup import backup
from envault.cli_tags import tags
from envault.cli_profiles import profiles
from envault.cli_templates import templates
from envault.cli_history import history
from envault.cli_ttl import ttl
from envault.cli_hooks import hooks
from envault.cli_snapshots import snapshots
from envault.cli_notes import notes
from envault.cli_reminders import reminders
from envault.cli_lint import lint
from envault.cli_compare import compare
from envault.cli_dependencies import dependencies


@click.group()
def main():
    """envault — encrypted environment variable manager."""


main.add_command(cli, "vault")
main.add_command(sharing)
main.add_command(audit)
main.add_command(rotation)
main.add_command(search)
main.add_command(backup)
main.add_command(tags)
main.add_command(profiles)
main.add_command(templates)
main.add_command(history)
main.add_command(ttl)
main.add_command(hooks)
main.add_command(snapshots)
main.add_command(notes)
main.add_command(reminders)
main.add_command(lint)
main.add_command(compare)
main.add_command(dependencies)


if __name__ == "__main__":
    main()
