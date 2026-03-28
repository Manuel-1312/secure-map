# Secure Map Codec

[![Face 2 Quality](https://github.com/Manuel-1312/secure-map/actions/workflows/face2-quality.yml/badge.svg)](https://github.com/Manuel-1312/secure-map/actions/workflows/face2-quality.yml)
[![Face 3 Release](https://github.com/Manuel-1312/secure-map/actions/workflows/face3-release.yml/badge.svg)](https://github.com/Manuel-1312/secure-map/actions/workflows/face3-release.yml)

## Visión extrema
Diseñamos un sistema de cartografía de grado militar: cada coordenada, ruta y mensaje se cifra con capas de AES-GCM+HKDF y viaja acompañada de firmas HMAC, auditoría firmada y rotación de claves por slot. Nada se comparte sin un keyring cifrado y un log firmado.

## Bajo el capó
| Componente | Propósito |
| --- | --- |
| `core/codec.py` | AES-GCM con HKDF para convertir coordenadas en tokens B64 con nonce aleatorio y metadata controlada. |
| `core/keyring.py` | Genera y guarda keyrings cifrados con `scrypt` (master) + HKDF (slots), cada uno con un `kid` y versión. |
| `core/package.py` | Arma paquetes de ruta+mensaje: envelope encryption + firma HMAC-SHA256 + timestamp + export para cliente. |
| `core/audit.py` | Registra cada acción crítica con un HMAC firmado (SHA-256) para detectar manipulación y replay. |
| `ui/console.py` | CLI confusa: rota claves, cifra/descifra, crea paquetes, inspecciona metadata y emite logs a prueba de guerra. |
| `docs/` | Documentación de seguridad, casos, políticas y guías operativas (incluye `SECURITY.md`, `USAGE.md`). |
| `tests/` | Validaciones del codec, keyring y paquetes cifrados para mantener invariantes criptográficos. |

## Estrategia segura
- Cada paquete lleva timestamp y HMAC; la verificación rechaza firmas inválidas y coteja el nonce para evitar replays.
- Las claves maestras se derivan con `scrypt` + sal única, y se rotan generando nuevos slots con metadata protegida.
- Todos los logs se firman con `core/audit.py`, creando cadenas de custodia que demuestran cualquier acceso.
- No hay secretos en claro: el CLI `ui/console.py` solo opera pasando passphrases que derivan claves temporales.

## Roadmap de largo alcance
- **Phase 1:** componentes core + CLI + docs de uso seguro.
- **Phase 2:** tests, lint y scripts de contribución (Face 2).
- **Phase 3:** pipeline CI y empaquetado PyPI/CLI corporativo.
- **Phase 4:** comunidad, casos de uso y monitoreo de seguridad.

## Face 2 — Calidad y flujo cifrado
- Agrega `requirements-dev.txt` y corre `pip install -r requirements-dev.txt` para preparar `ruff` y `pytest`.
- El workflow [Face 2 — Calidad](.github/workflows/face2-quality.yml) valida el código en Ubuntu (ruff + pytest) antes de mergear cualquier PR.
- Mantén actualizados los tests en `tests/` (codec, package) y crea nuevos casos si amplías la capa criptográfica.

## Face 3 — Release automation
- El workflow [Face 3 — Release automation](.github/workflows/face3-release.yml) recompila el CLI con PyInstaller y sube un ZIP como asset tras publicar un release.
- Consulta `docs/RELEASES.md` para el proceso completo y para documentar qué perfiles se usaron.
- El script `packaging/build-pyinstaller.sh` empaqueta `ui/console.py` junto con `core/` y `docs/` en un ejecutable multiplataforma.

## Cómo contribuir
Sigue `CONTRIBUTING.md`: abre un issue, crea rama, ejecuta `ruff check core ui tests` y `pytest tests`, y lanza el PR indicando qué Face toca.
