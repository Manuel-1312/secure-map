#!/usr/bin/env bash
set -euo pipefail
pyinstaller --clean --onefile \
  --name secure-map \
  --add-data "docs:docs" \
  --add-data "core:core" \
  ui/console.py
