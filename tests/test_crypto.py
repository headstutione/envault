"""Tests for envault.crypto encryption/decryption utilities."""

import pytest
from envault.crypto import encrypt, decrypt, encrypt_file, decrypt_file


PASSWORD = "super-secret-passphrase"
PLAINTEXT = "DB_HOST=localhost\nDB_PASS=hunter2\nAPI_KEY=abc123\n"


def test_encrypt_returns_bytes():
    result = encrypt(PLAINTEXT, PASSWORD)
    assert isinstance(result, bytes)


def test_encrypt_decrypt_roundtrip():
    encrypted = encrypt(PLAINTEXT, PASSWORD)
    decrypted = decrypt(encrypted, PASSWORD)
    assert decrypted == PLAINTEXT


def test_different_encryptions_produce_different_ciphertext():
    """Each call should use a fresh random salt."""
    enc1 = encrypt(PLAINTEXT, PASSWORD)
    enc2 = encrypt(PLAINTEXT, PASSWORD)
    assert enc1 != enc2


def test_wrong_password_raises_value_error():
    encrypted = encrypt(PLAINTEXT, PASSWORD)
    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt(encrypted, "wrong-password")


def test_corrupted_data_raises_value_error():
    encrypted = bytearray(encrypt(PLAINTEXT, PASSWORD))
    encrypted[20] ^= 0xFF  # flip bits in the ciphertext portion
    with pytest.raises(ValueError):
        decrypt(bytes(encrypted), PASSWORD)


def test_encrypt_file_decrypt_file_roundtrip(tmp_path):
    src = tmp_path / "env.txt"
    enc = tmp_path / "env.enc"
    out = tmp_path / "env_out.txt"

    src.write_text(PLAINTEXT, encoding="utf-8")
    encrypt_file(str(src), str(enc), PASSWORD)

    assert enc.exists()
    assert enc.read_bytes() != PLAINTEXT.encode()  # must be encrypted

    decrypt_file(str(enc), str(out), PASSWORD)
    assert out.read_text(encoding="utf-8") == PLAINTEXT


def test_encrypt_file_wrong_password(tmp_path):
    src = tmp_path / "env.txt"
    enc = tmp_path / "env.enc"
    out = tmp_path / "env_out.txt"

    src.write_text(PLAINTEXT, encoding="utf-8")
    encrypt_file(str(src), str(enc), PASSWORD)

    with pytest.raises(ValueError):
        decrypt_file(str(enc), str(out), "bad-password")
