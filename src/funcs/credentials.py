from __future__ import annotations

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

__all__ = ("decrypt_credential",)

with open("private.pem", "rb") as f:
    PRIVATE: rsa.RSAPrivateKey = serialization.load_pem_private_key(  # type: ignore
        f.read(), password=None
    )


def decrypt_credential(ciphertext: bytes, /) -> str:
    return PRIVATE.decrypt(ciphertext, padding.PKCS1v15()).decode("utf-8")
