from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import os
import base64
from datetime import datetime, timezone
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hmac import HMAC
from core.codec import encode, decode
from core.keyring import derive_subkey
from core.audit import log_event

NONCE_SIZE = 12
KEY_SIZE = 32

@dataclass
class Package:
    envelope: str
    route: List[Dict[str, str]]
    sig: str


def _encrypt(payload: bytes, key: bytes, info: bytes) -> str:
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    token = aesgcm.encrypt(nonce, payload, None)
    return base64.urlsafe_b64encode(nonce + token).decode("utf-8")


def _decrypt(token: str, key: bytes) -> bytes:
    raw = base64.urlsafe_b64decode(token.encode("utf-8"))
    nonce = raw[:NONCE_SIZE]
    ciphertext = raw[NONCE_SIZE:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)


def build_package(points: List[Dict[str, float]], message: str, master_key: bytes, audit_key: bytes) -> Package:
    route_key = derive_subkey(master_key, b"route")
    payload = b"|".join(encode(p['lat'], p['lon'], route_key).encode("utf-8") for p in points)
    timestamp = datetime.now(timezone.utc).isoformat()
    envelope = _encrypt(f"{message}|{timestamp}".encode("utf-8"), derive_subkey(master_key, b"msg"), b"envelope")
    route = [
        {"token": encode(p['lat'], p['lon'], route_key), "ts": timestamp}
        for p in points
    ]
    h = HMAC(audit_key, hashes.SHA256())
    h.update(route_key)
    h.update(envelope.encode("utf-8"))
    sig = base64.urlsafe_b64encode(h.finalize()).decode("utf-8")
    log_event({"envelope": envelope, "route_len": len(route), "timestamp": timestamp}, audit_key)
    return Package(envelope=envelope, route=route, sig=sig)


def inspect_package(pkg: Package, master_key: bytes, audit_key: bytes) -> Dict[str, str]:
    try:
        h = HMAC(audit_key, hashes.SHA256())
        route_key = derive_subkey(master_key, b"route")
        h.update(route_key)
        h.update(pkg.envelope.encode("utf-8"))
        h.verify(base64.urlsafe_b64decode(pkg.sig.encode("utf-8")))
    except Exception:
        raise ValueError("Signature mismatch or tampering detected")
    payload = _decrypt(pkg.envelope, derive_subkey(master_key, b"msg"))
    message, ts = payload.decode("utf-8").split("|")
    decoded = [decode(item["token"], route_key) for item in pkg.route]
    return {"message": message, "timestamp": ts, "points": str(decoded)}
