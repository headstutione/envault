"""CLI commands for managing key dependencies."""
import click
from envault.dependencies import (
    add_dependency, remove_dependency, get_dependencies,
    get_dependents, list_all_dependencies, clear_dependencies,
)

DEPS_FILE = ".envault_deps.json"


@click.group("deps")
def dependencies():
    """Manage dependencies between vault keys."""


@dependencies.command("add")
@click.argument("key")
@click.argument("depends_on")
def add_cmd(key, depends_on):
    """Add a dependency: KEY depends on DEPENDS_ON."""
    try:
        add_dependency(key, depends_on, DEPS_FILE)
        click.echo(f"Added: {key} -> {depends_on}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@dependencies.command("remove")
@click.argument("key")
@click.argument("depends_on")
def remove_cmd(key, depends_on):
    """Remove a dependency from KEY."""
    try:
        remove_dependency(key, depends_on, DEPS_FILE)
        click.echo(f"Removed: {key} -> {depends_on}")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)


@dependencies.command("list")
@click.argument("key")
def list_cmd(key):
    """List all dependencies of KEY."""
    deps = get_dependencies(key, DEPS_FILE)
    if not deps:
        click.echo(f"No dependencies for '{key}'.")
    else:
        for d in deps:
            click.echo(d)


@dependencies.command("dependents")
@click.argument("key")
def dependents_cmd(key):
    """List all keys that depend on KEY."""
    dependents = get_dependents(key, DEPS_FILE)
    if not dependents:
        click.echo(f"No keys depend on '{key}'.")
    else:
        for d in dependents:
            click.echo(d)


@dependencies.command("all")
def all_cmd():
    """Show all recorded dependencies."""
    all_deps = list_all_dependencies(DEPS_FILE)
    if not all_deps:
        click.echo("No dependencies recorded.")
    else:
        for key, deps in all_deps.items():
            click.echo(f"{key}: {', '.join(deps)}")
