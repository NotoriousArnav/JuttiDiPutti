# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

block_cipher = None

# Get the directory containing this spec file
spec_dir = Path(SPEC) if 'SPEC' in globals() else Path(__file__).parent

a = Analysis(
    ['main.py'],
    pathex=[str(spec_dir)],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('faces', 'faces'),
    ],
    hiddenimports=[
        'pygame',
        'pygame.mixer',
        'pygame.image',
        'pygame.display',
        'pygame.font',
        'pygame.transform',
        'pygame.math',
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PIL',
        'PIL.Image',
        'config',
        'assets',
        'entities',
        'game_state',
        'launcher',
        'json',
        'os',
        'sys',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, check=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version=None,
)