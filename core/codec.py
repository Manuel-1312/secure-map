from __future__ import annotations
from typing import Tuple
import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

NONCE_SIZE = 12


def derive_key(master: bytes, context: bytes = b"secure-map") -> bytes:
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=context)
    return hkdf.derive(master)


def encode(lat: float, lon: float, key: bytes) -> str:
    aesgcm = AESGCM(derive_key(key, context=b"encode"))
    nonce = os.urandom(NONCE_SIZE)
    payload = f"{lat:.6f}:{lon:.6f}".encode("utf-8")
    ct = aesgcm.encrypt(nonce, payload, None)
    return base64.urlsafe_b64encode(nonce + ct).decode("utf-8")


def decode(token: str, key: bytes) -> Tuple[float, float]:
    raw = base64.urlsafe_b64decode(token.encode("utf-8"))
    nonce = raw[:NONCE_SIZE]
    ct = raw[NONCE_SIZE:]
    aesgcm = AESGCM(derive_key(key, context=b"encode"))
    pt = aesgcm.decrypt(nonce, ct, None)
    lat_str, lon_str = pt.decode("utf-8").split(":")
    return float(lat_str), float(lon_str)
