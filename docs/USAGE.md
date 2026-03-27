# Uso básico

1. Instala dependencias: `pip install -r requirements.txt`.
2. Genera una clave maestra (modo interactivo o fixed) y pasa un passphrase.
3. Codifica una coordenada:
   ```bash
   python ui/console.py encode-point 40.7128 -74.0060 --passphrase="secreto"
   ```
4. Decodifica token:
   ```bash
   python ui/console.py decode-point <token> --passphrase="secreto"
   ```
5. Construye rutas mediante `core/mapper.py` y verifica firmas para integridad.
