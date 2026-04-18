"""Lint vault keys and values for common issues."""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List
from envault.vault import load_vault
from envault.crypto import decrypt

KEY_PATTERN = re.compile(r'^[A-Z][A-Z0-9_]*$')

@dataclass
class LintIssue:
    key: str
    level: str  # 'error' | 'warning'
    message: str

def lint_vault(vault_file: str, password: str) -> List[LintIssue]:
    """Return a list of lint issues found in the vault."""
    vault = load_vault(vault_file)
    if not vault:
        return []
    issues: List[LintIssue] = []
    for key, ciphertext in vault.items():
        # Key naming convention
        if not KEY_PATTERN.match(key):
            issues.append(LintIssue(key=key, level='warning',
                message=f"Key '{key}' does not follow UPPER_SNAKE_CASE convention"))
        # Decrypt and inspect value
        try:
            value = decrypt(ciphertext, password)
        except ValueError:
            issues.append(LintIssue(key=key, level='error',
                message=f"Key '{key}' could not be decrypted (wrong password or corrupt)"))
            continue
        if not value.strip():
            issues.append(LintIssue(key=key, level='warning',
                message=f"Key '{key}' has an empty or whitespace-only value"))
        if len(value) > 4096:
            issues.append(LintIssue(key=key, level='warning',
                message=f"Key '{key}' value is unusually large ({len(value)} chars)"))
    return issues
