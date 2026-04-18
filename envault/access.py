"""Access control: restrict which keys a given role/user can read or write."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_ACCESS_FILE = Path(".envault_access.json")


def _load_acl(access_file: Path) -> Dict:
    if not access_file.exists():
        return {}
    return json.loads(access_file.read_text())


def _save_acl(data: Dict, access_file: Path) -> None:
    access_file.write_text(json.dumps(data, indent=2))


def grant(role: str, key: str, permission: str, access_file: Path = DEFAULT_ACCESS_FILE) -> None:
    """Grant 'read' or 'write' permission on key to role."""
    if permission not in ("read", "write"):
        raise ValueError(f"Invalid permission '{permission}'; must be 'read' or 'write'")
    acl = _load_acl(access_file)
    acl.setdefault(role, {})
    acl[role].setdefault(key, [])
    if permission not in acl[role][key]:
        acl[role][key].append(permission)
    _save_acl(acl, access_file)


def revoke(role: str, key: str, permission: str, access_file: Path = DEFAULT_ACCESS_FILE) -> None:
    """Revoke a permission from a role for a key."""
    acl = _load_acl(access_file)
    perms = acl.get(role, {}).get(key, [])
    if permission in perms:
        perms.remove(permission)
    _save_acl(acl, access_file)


def can(role: str, key: str, permission: str, access_file: Path = DEFAULT_ACCESS_FILE) -> bool:
    """Return True if role has the given permission on key."""
    acl = _load_acl(access_file)
    return permission in acl.get(role, {}).get(key, [])


def list_permissions(role: str, access_file: Path = DEFAULT_ACCESS_FILE) -> Dict[str, List[str]]:
    """Return all key→permissions mapping for a role."""
    acl = _load_acl(access_file)
    return dict(acl.get(role, {}))


def delete_role(role: str, access_file: Path = DEFAULT_ACCESS_FILE) -> None:
    """Remove all permissions for a role."""
    acl = _load_acl(access_file)
    if role not in acl:
        raise KeyError(f"Role '{role}' not found")
    del acl[role]
    _save_acl(acl, access_file)


def list_roles(access_file: Path = DEFAULT_ACCESS_FILE) -> List[str]:
    """Return all defined roles."""
    return list(_load_acl(access_file).keys())
