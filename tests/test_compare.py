import pytest
from pathlib import Path
from click.testing import CliRunner
from envault.vault import save_vault
from envault.crypto import encrypt
from envault.compare import compare_vaults, compare_vault_dotenv
from envault.cli_compare import compare

PASSWORD = "secret"


def make_vault(path: Path, data: dict):
    vault = {k: encrypt(v.encode(), PASSWORD).hex() for k, v in data.items()}
    save_vault(path, vault)


@pytest.fixture
def vault_a(tmp_path):
    p = tmp_path / "a.vault"
    make_vault(p, {"KEY1": "val1", "SHARED": "same"})
    return p


@pytest.fixture
def vault_b(tmp_path):
    p = tmp_path / "b.vault"
    make_vault(p, {"KEY2": "val2", "SHARED": "same"})
    return p


@pytest.fixture
def vault_c(tmp_path):
    p = tmp_path / "c.vault"
    make_vault(p, {"SHARED": "different"})
    return p


def test_compare_vaults_only_a(vault_a, vault_b):
    results = compare_vaults(vault_a, PASSWORD, vault_b, PASSWORD)
    statuses = {r.key: r.status for r in results}
    assert statuses["KEY1"] == "only_a"


def test_compare_vaults_only_b(vault_a, vault_b):
    results = compare_vaults(vault_a, PASSWORD, vault_b, PASSWORD)
    statuses = {r.key: r.status for r in results}
    assert statuses["KEY2"] == "only_b"


def test_compare_vaults_match(vault_a, vault_b):
    results = compare_vaults(vault_a, PASSWORD, vault_b, PASSWORD)
    statuses = {r.key: r.status for r in results}
    assert statuses["SHARED"] == "match"


def test_compare_vaults_mismatch(vault_a, vault_c):
    results = compare_vaults(vault_a, PASSWORD, vault_c, PASSWORD)
    statuses = {r.key: r.status for r in results}
    assert statuses["SHARED"] == "mismatch"


def test_compare_vault_dotenv(vault_a, tmp_path):
    dotenv = tmp_path / ".env"
    dotenv.write_text("KEY1=val1\nEXTRA=hello\n")
    results = compare_vault_dotenv(vault_a, PASSWORD, dotenv)
    statuses = {r.key: r.status for r in results}
    assert statuses["KEY1"] == "match"
    assert statuses["EXTRA"] == "only_b"
    assert statuses["SHARED"] == "only_a"


def test_cli_vaults_command(vault_a, vault_b):
    runner = CliRunner()
    result = runner.invoke(
        compare, ["vaults", str(vault_a), str(vault_b),
                  "--password-a", PASSWORD, "--password-b", PASSWORD]
    )
    assert result.exit_code == 0
    assert "KEY1" in result.output
    assert "KEY2" in result.output


def test_cli_dotenv_command(vault_a, tmp_path):
    dotenv = tmp_path / ".env"
    dotenv.write_text("KEY1=val1\n")
    runner = CliRunner()
    result = runner.invoke(
        compare, ["dotenv", str(vault_a), str(dotenv), "--password", PASSWORD]
    )
    assert result.exit_code == 0
    assert "KEY1" in result.output
