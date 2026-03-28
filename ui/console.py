from __future__ import annotations
import typer
from typing import List
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from core.codec import encode, decode
from core.package import build_package, inspect_package, Package
from core.keyring import create_slot, save_keyring

app = typer.Typer()


def master_key(passphrase: str) -> bytes:
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"secure-map-ui")
    return hkdf.derive(passphrase.encode())


@app.command()
def encode_point(lat: float, lon: float, passphrase: str):
    key = master_key(passphrase)
    token = encode(lat, lon, key)
    typer.echo(token)


@app.command()
def decode_point(token: str, passphrase: str):
    key = master_key(passphrase)
    lat, lon = decode(token, key)
    typer.echo(f"{lat:.6f}, {lon:.6f}")


@app.command()
def rotate_key(kid: str, passphrase: str):
    slot = create_slot(passphrase, kid)
    save_keyring([slot], passphrase)
    typer.echo(f"Key {kid} rotated")


@app.command()
def create_package(points: List[str], message: str, passphrase: str, audit_pass: str, output: str = "package.json"):
    coords = [tuple(map(float, p.split(','))) for p in points]
    master = master_key(passphrase)
    audit = master_key(audit_pass)
    pkg = build_package([{'lat': lat, 'lon': lon} for lat, lon in coords], message, master, audit)
    data = {
        "envelope": pkg.envelope,
        "route": pkg.route,
        "sig": pkg.sig,
    }
    with open(output, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    typer.echo(f"Package stored in {output}")


@app.command()
def inspect(path: str, passphrase: str, audit_pass: str):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    master = master_key(passphrase)
    audit = master_key(audit_pass)
    pkg = Package(envelope=data["envelope"], route=data["route"], sig=data["sig"])
    info = inspect_package(pkg, master, audit)
    typer.echo(json.dumps(info, indent=2))

if __name__ == "__main__":
    app()
