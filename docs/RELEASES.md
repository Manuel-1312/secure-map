# Procedimiento de releases (Face 3)

1. Etiqueta la versión (`v0.2.0`, etc.) y marca un release draft en GitHub.
2. La acción `Face 3 — Release automation` recompila el CLI con PyInstaller y sube el ZIP como asset.
3. Añade en la descripción las rutas/mesajes cifrados que muestra el release y los perfiles de casos usados.
4. Mantén el changelog en `README.md` y apunta a este documento cuando publiques para que sepan cómo reproducir el build.
