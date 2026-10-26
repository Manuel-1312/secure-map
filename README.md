# Secure Map Codec

> **Archivado.** Prototipo personal, sin mantenimiento. Es un ejercicio de criptografía aplicada y no tiene auditoría externa: no lo uses para proteger datos reales.

Cifra coordenadas y rutas en tokens y las empaqueta con firma, usando primitivas estándar de la librería `cryptography`.

## Qué hay

| Ruta | Contenido |
| --- | --- |
| `core/codec.py` | AES-GCM con clave derivada por HKDF; convierte coordenadas en tokens Base64 |
| `core/keyring.py` | Keyring cifrado con clave maestra derivada por `scrypt` y slots rotables |
| `core/package.py` | Paquete ruta + mensaje con cifrado de sobre, HMAC-SHA256 y timestamp |
| `core/audit.py` | Log de acciones encadenado con HMAC para detectar manipulación |
| `ui/console.py` | CLI para rotar claves, cifrar, descifrar e inspeccionar paquetes |
| `tests/` | Tests del codec y de los paquetes |

## Uso

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest tests
python ui/console.py --help
```

Más detalle en `docs/USAGE.md` y `docs/SECURITY.md`.
