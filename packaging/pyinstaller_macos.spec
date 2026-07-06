# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["../prompter/app.py"],
    pathex=[".."],
    binaries=[],
    datas=[("../img/PrompterLogo_1024.icns", "img")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Prompter",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name="Prompter.app",
    icon="../img/PrompterLogo_1024.icns",
    bundle_identifier="com.Prompter.app",
)
