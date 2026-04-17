"""Encryption and decryption utilities for envault using Fernet symmetric encryption."""

import os
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


SALT_SIZE = 16
ITERATIONS = 390000


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt(plaintext: str, password: str) -> bytes:
    """
    Encrypt a plaintext string with a password.
    Returns salt + encrypted bytes.
    """
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    token = Fernet(key).encrypt(plaintext.encode())
    return salt + token


def decrypt(data: bytes, password: str) -> str:
    """
    Decrypt data produced by `encrypt`.
    Raises ValueError on wrong password or corrupted data.
    """
    salt = data[:SALT_SIZE]
    token = data[SALT_SIZE:]
    key = derive_key(password, salt)
    try:
        return Fernet(key).decrypt(token).decode()
    except InvalidToken as exc:
        raise ValueError("Decryption failed: invalid password or corrupted data.") from exc


def encrypt_file(src_path: str, dst_path: str, password: str) -> None:
    """Read a plaintext file and write its encrypted version."""
    with open(src_path, "r", encoding="utf-8") as f:
        plaintext = f.read()
    encrypted = encrypt(plaintext, password)
    with open(dst_path, "wb") as f:
        f.write(encrypted)


def decrypt_file(src_path: str, dst_path: str, password: str) -> None:
    """Read an encrypted file and write its decrypted version."""
    with open(src_path, "rb") as f:
        data = f.read()
    plaintext = decrypt(data, password)
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(plaintext)
