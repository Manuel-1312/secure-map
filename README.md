# Secure Map Codec

## Visión
Un sistema de cartografía avanzada que codifica y descodifica localizaciones y rutas con técnicas criptográficas y estructuras de datos geoespaciales. El objetivo es ofrecer un módulo Python que permita generar mapas cifrados, compartirlos con confianza y reconstruirlos en sistemas autorizados.

## Componentes
- `core/codec.py`: AES-GCM + HKDF para cifrar coordenadas y generar tokens B64 con nonce random.
- `core/keyring.py`: gestor de keyrings cifrados que deriva claves maestras con scrypt/HKDF y guarda slots con metadata (`kid`, versión, salt).
- `core/package.py`: genera "paquetes" que contienen ruta + mensaje, prepara envelope encryption y añade firmas HMAC-SHA256 (con auditoría).
- `core/audit.py`: registro firmado (SHA-256/HMAC) por cada operación crítica para detectar manipulación y replay.
- `ui/console.py`: CLI avanzada para rotar claves, cifrar/descifrar coordenadas o paquetes completos, e inspeccionar metadata.
- `docs/`: especificaciones criptográficas, API, políticas y guías de uso/seguridad.
- `tests/`: validaciones criptográficas del codec y del paquete.

## Seguridad militar
- Claves maestras derivadas con `scrypt` + sal única, y subclaves generadas con HKDF para cada uso (route, message, audit).
- Cada paquete incluye timestamp, HMAC y nonce; la verificación rechaza firmas inválidas y detecta replay.
- Auditoría firmada (SHA-256/HMAC) en `core/audit.py` impide manipulación silenciosa y proporciona cadena de custodia.
- Rotación de claves y almacenamiento cifrado en `core/keyring.py` permite suspender slots comprometidos sin perder acceso a datos anteriores.

## Roadmap inicial
1. Face 1: core codec + CLI + docs mínimos.
2. Face 2: tests, lint, contribución responsable.
3. Face 3: pipeline CI (lint/test) y packaging en PyPI.
4. Face 4: docs de comunidad y casos de uso autorizados.
