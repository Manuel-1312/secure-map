from __future__ import annotations
import typer
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from core.codec import encode, decode

app = typer.Typer()


def get_master_key(passphrase: str) -> bytes:
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"secure-map-ui")
    return hkdf.derive(passphrase.encode())


@app.command()
def encode_point(lat: float, lon: float, passphrase: str):
    key = get_master_key(passphrase)
    token = encode(lat, lon, key)
    typer.echo(token)


@app.command()
def decode_point(token: str, passphrase: str):
    key = get_master_key(passphrase)
    lat, lon = decode(token, key)
    typer.echo(f"{lat:.6f}, {lon:.6f}")
