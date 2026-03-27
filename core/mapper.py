from __future__ import annotations
from typing import List, Tuple
from datetime import datetime
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.mac import HMAC
from core.codec import encode

NONCE_KEY = b"mapper-signature"


def derive_key(master: bytes, context: bytes) -> bytes:
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=context)
    return hkdf.derive(master)


def signature(data: bytes, key: bytes) -> bytes:
    h = HMAC(derive_key(key, context=NONCE_KEY), hashes.SHA256())
    h.update(data)
    return h.finalize()


def build_route(points: List[Tuple[float, float]], key: bytes) -> List[dict]:
    encoded = [encode(lat, lon, key) for lat, lon in points]
    payload = b"|".join(e.encode("utf-8") for e in encoded)
    sig = signature(payload, key)
    timestamp = datetime.utcnow().isoformat()
    return [
        {"token": token, "timestamp": timestamp, "sig": base64.urlsafe_b64encode(sig).decode("utf-8")}
        for token in encoded
    ]


def verify_route(route: List[dict], key: bytes) -> bool:
    payload = b"|".join(item["token"].encode("utf-8") for item in route)
    expected = signature(payload, key)
    return any(base64.urlsafe_b64decode(item["sig"]) == expected for item in route)
