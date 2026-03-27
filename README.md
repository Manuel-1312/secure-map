# Secure Map Codec

## Visión
Un sistema de cartografía avanzada que codifica y descodifica localizaciones y rutas con técnicas criptográficas y estructuras de datos geoespaciales. El objetivo es ofrecer un módulo Python que permita generar mapas cifrados, compartirlos con confianza y reconstruirlos en sistemas autorizados.

## Componentes
- `core/codec.py`: codifica coordenadas (lat/lon) en tokens cifrados y decodifica con claves.
- `core/mapper.py`: construye rutas, valida topología y guarda metadata segura.
- `ui/console.py`: CLI mínima para encriptar/descifrar rutas y exportar.
- `docs/`: especificaciones criptográficas, API y políticas de uso.
- `tests/`: validaciones de codec, mapas y permisos.

## Seguridad
- Usa Fernet (AES-128) + HKDF para derivar claves por proyecto.
- Incluye validaciones para evitar manipulación de coordenadas y timestamp/nonce contra duplicados.

## Roadmap inicial
1. Face 1: core codec + CLI + docs mínimos.
2. Face 2: tests, lint, contribución responsable.
3. Face 3: pipeline CI (lint/test) y packaging en PyPI.
4. Face 4: docs de comunidad y casos de uso autorizados.
