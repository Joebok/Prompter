#!/usr/bin/env bash
set -euo pipefail

export PYINSTALLER_CONFIG_DIR="${PYINSTALLER_CONFIG_DIR:-"$PWD/build/pyinstaller-cache"}"

python3 -m pip install -U pip
python3 -m pip install -e '.[dev]'
python3 -m PyInstaller packaging/pyinstaller_macos.spec --clean --noconfirm
