$ErrorActionPreference = "Stop"

python3 -m pip install -U pip
python3 -m pip install -e ".[dev]"
python3 -m PyInstaller packaging/pyinstaller_windows.spec --clean --noconfirm
