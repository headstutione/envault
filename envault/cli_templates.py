import click
from envault.templates import create_template, delete_template, list_templates, apply_template


@click.group()
def templates():
    """Manage variable templates."""
    pass


@templates.command("create")
@click.argument("name")
@click.argument("keys", nargs=-1, required=True)
@click.option("--file", "tf", default=".envault_templates.json", show_default=True)
def create_cmd(name, keys, tf):
    """Create a template with required KEY names."""
    try:
        create_template(name, list(keys), templates_file=tf)
        click.echo(f"Template '{name}' created with keys: {', '.join(keys)}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@templates.command("delete")
@click.argument("name")
@click.option("--file", "tf", default=".envault_templates.json", show_default=True)
def delete_cmd(name, tf):
    """Delete a template by name."""
    try:
        delete_template(name, templates_file=tf)
        click.echo(f"Template '{name}' deleted.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)


@templates.command("list")
@click.option("--file", "tf", default=".envault_templates.json", show_default=True)
def list_cmd(tf):
    """List all templates."""
    tmpls = list_templates(templates_file=tf)
    if not tmpls:
        click.echo("No templates defined.")
    else:
        for name, keys in tmpls.items():
            click.echo(f"{name}: {', '.join(keys)}")


@templates.command("apply")
@click.argument("name")
@click.option("--vault", "vault_file", default=".envault.json", show_default=True)
@click.option("--file", "tf", default=".envault_templates.json", show_default=True)
@click.option("--password", prompt=True, hide_input=True)
def apply_cmd(name, vault_file, tf, password):
    """Check vault has all keys required by template."""
    try:
        missing = apply_template(name, vault_file=vault_file, password=password, templates_file=tf)
        if missing:
            click.echo(f"Missing keys for template '{name}': {', '.join(missing)}", err=True)
        else:
            click.echo(f"All keys for template '{name}' are present.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)
