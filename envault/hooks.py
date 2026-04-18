"""Pre/post hooks for vault operations."""
from __future__ import annotations
import json
from pathlib import Path
from typing import List, Optional

DEFAULT_HOOKS_FILE = Path(".envault_hooks.json")


def _load_hooks(hooks_file: Path = DEFAULT_HOOKS_FILE) -> dict:
    if not hooks_file.exists():
        return {}
    with hooks_file.open() as f:
        return json.load(f)


def _save_hooks(data: dict, hooks_file: Path = DEFAULT_HOOKS_FILE) -> None:
    with hooks_file.open("w") as f:
        json.dump(data, f, indent=2)


def set_hook(event: str, command: str, hooks_file: Path = DEFAULT_HOOKS_FILE) -> None:
    """Register a shell command to run on a given event."""
    valid_events = {"pre-set", "post-set", "pre-delete", "post-delete", "post-rotate"}
    if event not in valid_events:
        raise ValueError(f"Unknown event '{event}'. Valid: {sorted(valid_events)}")
    data = _load_hooks(hooks_file)
    data[event] = command
    _save_hooks(data, hooks_file)


def remove_hook(event: str, hooks_file: Path = DEFAULT_HOOKS_FILE) -> bool:
    """Remove a hook. Returns True if it existed."""
    data = _load_hooks(hooks_file)
    if event not in data:
        return False
    del data[event]
    _save_hooks(data, hooks_file)
    return True


def get_hook(event: str, hooks_file: Path = DEFAULT_HOOKS_FILE) -> Optional[str]:
    return _load_hooks(hooks_file).get(event)


def list_hooks(hooks_file: Path = DEFAULT_HOOKS_FILE) -> List[dict]:
    data = _load_hooks(hooks_file)
    return [{"event": k, "command": v} for k, v in sorted(data.items())]


def run_hook(event: str, hooks_file: Path = DEFAULT_HOOKS_FILE) -> Optional[str]:
    """Execute the hook command for the event. Returns output or None."""
    import subprocess
    cmd = get_hook(event, hooks_file)
    if cmd is None:
        return None
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Hook '{event}' failed: {result.stderr.strip()}")
    return result.stdout.strip()
