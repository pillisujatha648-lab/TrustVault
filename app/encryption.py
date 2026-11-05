
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def get_encryption_key():
    key = os.environ.get("ENCRYPTION_KEY")

    if not key:
        raise RuntimeError("ENCRYPTION_KEY is not configured.")

    key = bytes.fromhex(key)

    if len(key) != 32:
        raise RuntimeError("Encryption key must be 32 bytes.")

    return key


def encrypt_file(file_data):
    key = get_encryption_key()

    aes = AESGCM(key)

    nonce = os.urandom(12)

    encrypted_data = aes.encrypt(
        nonce,
        file_data,
        None
    )

    return nonce + encrypted_data


def decrypt_file(encrypted_data):
    key = get_encryption_key()

    aes = AESGCM(key)

    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    return aes.decrypt(
        nonce,
        ciphertext,
        None
    )
