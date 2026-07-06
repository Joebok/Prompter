$ErrorActionPreference = "Stop"

python -m pip install -U pip
python -m pip install -e ".[dev]"
python -m PyInstaller packaging/pyinstaller_windows.spec --clean --noconfirm
