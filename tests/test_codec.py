from core.codec import encode, decode

def test_roundtrip_returns_same_point():
    key = b"secret1234567890"
    token = encode(40.7128, -74.0060, key)
    lat, lon = decode(token, key)
    assert abs(lat - 40.7128) < 1e-6
    assert abs(lon + 74.0060) < 1e-6
