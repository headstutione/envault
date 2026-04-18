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
from envault.cli_lint import lint
from envault.cli_history import history
from envault.cli_compare import compare


cli.add_command(sharing)
cli.add_command(audit)
cli.add_command(rotation)
cli.add_command(search)
cli.add_command(backup)
cli.add_command(tags)
cli.add_command(profiles)
cli.add_command(templates)
cli.add_command(lint)
cli.add_command(history)
cli.add_command(compare)


if __name__ == "__main__":
    cli()
