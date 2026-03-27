from __future__ import annotations
import json
import os
from datetime import datetime
from typing import Dict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hmac import HMAC

AUDIT_LOG = "audit.log"


def log_event(event: Dict[str, str], key: bytes):
    payload = json.dumps({**event, "ts": datetime.utcnow().isoformat()}).encode("utf-8")
    h = HMAC(key, hashes.SHA256())
    h.update(payload)
    sig = h.finalize().hex()
    entry = {"event": event, "sig": sig}
    with open(AUDIT_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def verify_event(payload: Dict[str, str], key: bytes, sig: str) -> bool:
    h = HMAC(key, hashes.SHA256())
    h.update(json.dumps(payload).encode("utf-8"))
    try:
        h.verify(bytes.fromhex(sig))
        return True
    except Exception:
        return False
