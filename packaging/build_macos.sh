#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -U pip
python3 -m pip install -e '.[dev]'
python3 -m PyInstaller packaging/pyinstaller_macos.spec --clean --noconfirm
