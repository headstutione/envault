import pytest
from pathlib import Path
from envault.profiles import (
    create_profile, delete_profile, assign_key,
    unassign_key, get_profile_keys, list_profiles,
)


@pytest.fixture
def pf(tmp_path):
    return tmp_path / "profiles.json"


def test_list_profiles_empty_when_missing(pf):
    assert list_profiles(pf) == []


def test_create_profile(pf):
    create_profile("dev", pf)
    assert "dev" in list_profiles(pf)


def test_create_duplicate_profile_raises(pf):
    create_profile("dev", pf)
    with pytest.raises(ValueError, match="already exists"):
        create_profile("dev", pf)


def test_delete_profile(pf):
    create_profile("dev", pf)
    delete_profile("dev", pf)
    assert "dev" not in list_profiles(pf)


def test_delete_missing_profile_raises(pf):
    with pytest.raises(KeyError):
        delete_profile("ghost", pf)


def test_assign_key_to_profile(pf):
    create_profile("dev", pf)
    assign_key("dev", "DATABASE_URL", pf)
    assert "DATABASE_URL" in get_profile_keys("dev", pf)


def test_assign_key_no_duplicates(pf):
    create_profile("dev", pf)
    assign_key("dev", "KEY", pf)
    assign_key("dev", "KEY", pf)
    assert get_profile_keys("dev", pf).count("KEY") == 1


def test_unassign_key(pf):
    create_profile("dev", pf)
    assign_key("dev", "KEY", pf)
    unassign_key("dev", "KEY", pf)
    assert "KEY" not in get_profile_keys("dev", pf)


def test_assign_key_missing_profile_raises(pf):
    with pytest.raises(KeyError):
        assign_key("ghost", "KEY", pf)


def test_multiple_profiles(pf):
    create_profile("dev", pf)
    create_profile("prod", pf)
    names = list_profiles(pf)
    assert "dev" in names
    assert "prod" in names


def test_get_profile_keys_missing_profile_raises(pf):
    with pytest.raises(KeyError):
        get_profile_keys("nope", pf)
