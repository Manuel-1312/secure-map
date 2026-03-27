from core.package import build_package, inspect_package, Package
from core.keyring import derive_subkey

def test_package_roundtrip():
    master = b"supersecretmasterkey1234567890"
    audit = b"auditingtoolongkey1234567890"
    points = [{'lat': 40.0, 'lon': -70.0}, {'lat': 41.0, 'lon': -71.0}]
    pkg = build_package(points, "Mission Alpha", master, audit)
    assert isinstance(pkg, Package)
    info = inspect_package(pkg, master, audit)
    assert info["message"] == "Mission Alpha"
    assert len(info["points"]) == len(points)
