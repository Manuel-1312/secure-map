# Secure Map Codec

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
- **Phase 2:** tests, lint y scripts de contribución presente.
- **Phase 3:** pipeline CI y empaquetado PyPI/CLI corporativo.
- **Phase 4:** comunidad, casos de uso y monitoreo de seguridad.
