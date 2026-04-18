"""Export vault variables to shell-sourceable .env format."""
from __future__ import annotations

from pathlib import Path

from envault.vault import load_vault, get_variable


def export_dotenv(vault_path: Path, password: str, output_path: Path) -> int:
    """Write all vault variables to a .env file. Returns count of variables written."""
    vault = load_vault(vault_path)
    if not vault:
        raise ValueError("Vault is empty — nothing to export.")

    lines = []
    for key in sorted(vault.keys()):
        value = get_variable(vault_path, key, password)
        if value is None:
            continue
        escaped = value.replace('"', '\\"')
        lines.append(f'{key}="{escaped}"')

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


def import_dotenv(vault_path: Path, password: str, input_path: Path) -> int:
    """Read a .env file and store variables into the vault. Returns count imported."""
    from envault.vault import set_variable

    if not input_path.exists():
        raise FileNotFoundError(f".env file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")
    count = 0
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, raw_value = line.partition("=")
        key = key.strip()
        raw_value = raw_value.strip()
        # Strip surrounding quotes
        if len(raw_value) >= 2 and raw_value[0] == '"' and raw_value[-1] == '"':
            raw_value = raw_value[1:-1].replace('\\"', '"')
        elif len(raw_value) >= 2 and raw_value[0] == "'" and raw_value[-1] == "'":
            raw_value = raw_value[1:-1]
        if key:
            set_variable(vault_path, key, raw_value, password)
            count += 1
    return count
