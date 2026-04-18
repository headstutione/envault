import pytest
from pathlib import Path
from envault.templates import (
    create_template, delete_template, list_templates,
    get_template, check_vault_against_template,
)


@pytest.fixture
def tf(tmp_path):
    return tmp_path / "templates.json"


def test_list_templates_empty_when_missing(tf):
    assert list_templates(tf) == {}


def test_create_template(tf):
    create_template("web", ["DATABASE_URL", "SECRET_KEY"], tf)
    assert "web" in list_templates(tf)
    assert get_template("web", tf) == ["DATABASE_URL", "SECRET_KEY"]


def test_create_duplicate_raises(tf):
    create_template("web", ["A"], tf)
    with pytest.raises(ValueError, match="already exists"):
        create_template("web", ["B"], tf)


def test_create_empty_keys_raises(tf):
    with pytest.raises(ValueError, match="at least one key"):
        create_template("empty", [], tf)


def test_delete_template(tf):
    create_template("web", ["A"], tf)
    delete_template("web", tf)
    assert "web" not in list_templates(tf)


def test_delete_missing_raises(tf):
    with pytest.raises(KeyError):
        delete_template("ghost", tf)


def test_get_template_missing_raises(tf):
    with pytest.raises(KeyError):
        get_template("nope", tf)


def test_check_vault_all_present(tf):
    create_template("web", ["A", "B"], tf)
    result = check_vault_against_template("web", ["A", "B"], tf)
    assert result["missing"] == []
    assert result["extra"] == []


def test_check_vault_missing_keys(tf):
    create_template("web", ["A", "B", "C"], tf)
    result = check_vault_against_template("web", ["A"], tf)
    assert result["missing"] == ["B", "C"]


def test_check_vault_extra_keys(tf):
    create_template("web", ["A"], tf)
    result = check_vault_against_template("web", ["A", "B", "C"], tf)
    assert result["extra"] == ["B", "C"]
