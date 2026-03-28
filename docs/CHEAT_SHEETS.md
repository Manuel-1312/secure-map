# Cheat Sheets

- **Rotar clave de misión:** `python ui/console.py rotate-key mission-alpha --passphrase="alpha"` y guarda el nuevo keyring cifrado.
- **Crear package seguro:** `python ui/console.py create-package 40.7128,-74.0060 41.2033,-77.1945 "Convoy safe" --passphrase=alpha --audit-pass=audit123 --output=mission-alpha.json`.
- **Inspeccionar paquete:** `python ui/console.py inspect mission-alpha.json --passphrase=alpha --audit-pass=audit123` y valida el log firmado.
