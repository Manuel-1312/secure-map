# Case Study — Mission Alpha

- **Objetivo:** proteger la línea de convoy en el corredor atlántico (coordenadas 40.7128,-74.0060 → 41.2033,-77.1945). El control de misión usa Secure Map para compartir rutas cifradas sin exponer metadata en texto plano.
- **Flujo:** generamos un keyring rotado con `ui/console.py rotate-key mission-alpha`, luego construimos el paquete cifrado `ui/console.py create-package 40.7128,-74.0060 41.2033,-77.1945 "Convoy safe" --passphrase=alpha --audit-pass=audit123`.
- **Resultado:** el archivo `package.json` contiene el envelope cifrado y la ruta firmada (HMAC). El equipo receptor corre `ui/console.py inspect package.json --passphrase=alpha --audit-pass=audit123` y verifica que la auditoría logueada coincide (`audit.log`).
- **Lecciones:** cada package añade timestamp y sig; al rotar la clave se invalida el slot anterior y se actualiza el log; el JSON resultante se guarda en `docs/case-studies/mission-alpha-raw.json` para reproducir.
