import pytest
from envault.dependencies import (
    add_dependency, remove_dependency, get_dependencies,
    get_dependents, list_all_dependencies, clear_dependencies,
)


@pytest.fixture
def df(tmp_path):
    return str(tmp_path / "deps.json")


def test_get_dependencies_returns_empty_when_missing(df):
    assert get_dependencies("KEY_A", df) == []


def test_add_dependency_creates_entry(df):
    add_dependency("KEY_A", "KEY_B", df)
    assert "KEY_B" in get_dependencies("KEY_A", df)


def test_add_dependency_no_duplicates(df):
    add_dependency("KEY_A", "KEY_B", df)
    add_dependency("KEY_A", "KEY_B", df)
    assert get_dependencies("KEY_A", df).count("KEY_B") == 1


def test_add_multiple_dependencies(df):
    add_dependency("KEY_A", "KEY_B", df)
    add_dependency("KEY_A", "KEY_C", df)
    deps = get_dependencies("KEY_A", df)
    assert "KEY_B" in deps and "KEY_C" in deps


def test_self_dependency_raises(df):
    with pytest.raises(ValueError):
        add_dependency("KEY_A", "KEY_A", df)


def test_remove_dependency(df):
    add_dependency("KEY_A", "KEY_B", df)
    remove_dependency("KEY_A", "KEY_B", df)
    assert get_dependencies("KEY_A", df) == []


def test_remove_missing_dependency_raises(df):
    with pytest.raises(KeyError):
        remove_dependency("KEY_A", "KEY_B", df)


def test_get_dependents(df):
    add_dependency("KEY_A", "KEY_B", df)
    add_dependency("KEY_C", "KEY_B", df)
    dependents = get_dependents("KEY_B", df)
    assert "KEY_A" in dependents and "KEY_C" in dependents


def test_get_dependents_empty(df):
    assert get_dependents("KEY_X", df) == []


def test_list_all_dependencies(df):
    add_dependency("KEY_A", "KEY_B", df)
    add_dependency("KEY_C", "KEY_D", df)
    all_deps = list_all_dependencies(df)
    assert "KEY_A" in all_deps and "KEY_C" in all_deps


def test_clear_dependencies(df):
    add_dependency("KEY_A", "KEY_B", df)
    clear_dependencies("KEY_A", df)
    assert get_dependencies("KEY_A", df) == []
