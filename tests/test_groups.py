import pytest
from envault.groups import (
    create_group, delete_group, add_key_to_group,
    remove_key_from_group, get_group_keys, list_groups
)


@pytest.fixture
def gf(tmp_path):
    return str(tmp_path / "groups.json")


def test_list_groups_empty_when_missing(gf):
    assert list_groups(gf) == []


def test_create_group(gf):
    create_group("backend", ["DB_URL", "DB_PASS"], gf)
    assert "backend" in list_groups(gf)


def test_create_group_deduplicates_keys(gf):
    create_group("g", ["A", "A", "B"], gf)
    assert get_group_keys("g", gf) == ["A", "B"]


def test_create_duplicate_group_raises(gf):
    create_group("g", ["A"], gf)
    with pytest.raises(ValueError, match="already exists"):
        create_group("g", ["B"], gf)


def test_create_empty_keys_raises(gf):
    with pytest.raises(ValueError, match="at least one key"):
        create_group("g", [], gf)


def test_create_empty_name_raises(gf):
    with pytest.raises(ValueError, match="must not be empty"):
        create_group("", ["A"], gf)


def test_delete_group(gf):
    create_group("g", ["A"], gf)
    delete_group("g", gf)
    assert "g" not in list_groups(gf)


def test_delete_missing_group_raises(gf):
    with pytest.raises(KeyError):
        delete_group("nope", gf)


def test_add_key_to_group(gf):
    create_group("g", ["A"], gf)
    add_key_to_group("g", "B", gf)
    assert "B" in get_group_keys("g", gf)


def test_add_key_no_duplicates(gf):
    create_group("g", ["A"], gf)
    add_key_to_group("g", "A", gf)
    assert get_group_keys("g", gf).count("A") == 1


def test_remove_key_from_group(gf):
    create_group("g", ["A", "B"], gf)
    remove_key_from_group("g", "A", gf)
    assert "A" not in get_group_keys("g", gf)


def test_remove_missing_key_raises(gf):
    create_group("g", ["A"], gf)
    with pytest.raises(KeyError):
        remove_key_from_group("g", "Z", gf)


def test_get_group_keys_missing_group_raises(gf):
    with pytest.raises(KeyError):
        get_group_keys("nope", gf)
