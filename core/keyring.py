from __future__ import annotations
from dataclasses import dataclass
import json
import os
from typing import Dict, List
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEYRING_FILE = "keyring.json"

@dataclass
class KeySlot:
    kid: str
    salt: bytes
    material: bytes
    version: int


def derive_root(passphrase: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(passphrase.encode())


def derive_subkey(root: bytes, info: bytes) -> bytes:
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=info)
    return hkdf.derive(root)


def create_slot(passphrase: str, kid: str, version: int = 1) -> KeySlot:
    salt = os.urandom(16)
    root = derive_root(passphrase, salt)
    material = derive_subkey(root, f"slot-{kid}-{version}".encode())
    return KeySlot(kid=kid, salt=salt, material=material, version=version)


def encrypt_keyring(slots: List[KeySlot], master_key: bytes) -> bytes:
    aesgcm = AESGCM(master_key)
    nonce = os.urandom(12)
    data = json.dumps([
        {"kid": slot.kid, "salt": slot.salt.hex(), "material": slot.material.hex(), "version": slot.version}
        for slot in slots
    ]).encode("utf-8")
    return nonce + aesgcm.encrypt(nonce, data, None)


def decrypt_keyring(blob: bytes, master_key: bytes) -> List[KeySlot]:
    aesgcm = AESGCM(master_key)
    nonce = blob[:12]
    ct = blob[12:]
    raw = aesgcm.decrypt(nonce, ct, None)
    parsed = json.loads(raw.decode("utf-8"))
    return [KeySlot(kid=item["kid"], salt=bytes.fromhex(item["salt"].strip()), material=bytes.fromhex(item["material"].strip()), version=item["version"]) for item in parsed]


def save_keyring(slots: List[KeySlot], passphrase: str):
    master = derive_root(passphrase, b"ring-lock")
    blob = encrypt_keyring(slots, master)
    with open(KEYRING_FILE, "wb") as fh:
        fh.write(blob)


def load_keyring(passphrase: str) -> List[KeySlot]:
    with open(KEYRING_FILE, "rb") as fh:
        blob = fh.read()
    master = derive_root(passphrase, b"ring-lock")
    return decrypt_keyring(blob, master)
