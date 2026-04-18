"""Tests for envault.sharing module."""

import json
import pytest
from pathlib import Path

from envault.sharing import export_bundle, import_bundle
from envault.vault import save_vault

PASSWORD = "team-secret-42"


@pytest.fixture
def vault_file(tmp_path):
    return tmp_path / ".envault"


@pytest.fixture
def bundle_file(tmp_path):
    return tmp_path / "bundle.json"


def test_export_creates_bundle_file(vault_file, bundle_file):
    save_vault(vault_file, {"API_KEY": "abc", "DB_URL": "postgres://"})
    export_bundle(vault_file, PASSWORD, bundle_file)
    assert bundle_file.exists()
    data = json.loads(bundle_file.read_text())
    assert data["version"] == 1
    assert "data" in data


def test_export_empty_vault_raises(vault_file, bundle_file):
    with pytest.raises(ValueError, match="empty"):
        export_bundle(vault_file, PASSWORD, bundle_file)


def test_import_roundtrip(vault_file, bundle_file, tmp_path):
    save_vault(vault_file, {"API_KEY": "abc", "SECRET": "xyz"})
    export_bundle(vault_file, PASSWORD, bundle_file)

    target_vault = tmp_path / ".envault2"
    result = import_bundle(bundle_file, PASSWORD, target_vault)

    assert set(result["added"]) == {"API_KEY", "SECRET"}
    assert result["skipped"] == []


def test_import_skips_existing_keys_by_default(vault_file, bundle_file, tmp_path):
    save_vault(vault_file, {"API_KEY": "abc", "NEW_KEY": "new"})
    export_bundle(vault_file, PASSWORD, bundle_file)

    target_vault = tmp_path / ".envault2"
    save_vault(target_vault, {"API_KEY": "original"})

    result = import_bundle(bundle_file, PASSWORD, target_vault)
    assert "API_KEY" in result["skipped"]
    assert "NEW_KEY" in result["added"]


def test_import_overwrite_flag(vault_file, bundle_file, tmp_path):
    save_vault(vault_file, {"API_KEY": "new-value"})
    export_bundle(vault_file, PASSWORD, bundle_file)

    target_vault = tmp_path / ".envault2"
    save_vault(target_vault, {"API_KEY": "old-value"})

    result = import_bundle(bundle_file, PASSWORD, target_vault, overwrite=True)
    assert "API_KEY" in result["added"]
    assert result["skipped"] == []


def test_import_wrong_password_raises(vault_file, bundle_file, tmp_path):
    save_vault(vault_file, {"KEY": "val"})
    export_bundle(vault_file, PASSWORD, bundle_file)

    target = tmp_path / ".envault2"
    with pytest.raises(ValueError):
        import_bundle(bundle_file, "wrong-password", target)


def test_import_unsupported_version_raises(bundle_file, tmp_path):
    bundle_file.write_text(json.dumps({"version": 99, "data": ""}))
    with pytest.raises(ValueError, match="Unsupported bundle version"):
        import_bundle(bundle_file, PASSWORD, tmp_path / ".envault")
