# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller specification file for PDF OCR Desktop Application
This creates a standalone executable with all dependencies bundled.
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all data files for packages that need them
datas = []

# Add pytesseract data files if any
datas += collect_data_files('pytesseract', include_py_files=True)

# Add any additional data files from the project
# Add Poppler binaries if they exist in the project
if os.path.exists('poppler'):
    datas += [('poppler', 'poppler')]

# Collect hidden imports
hiddenimports = []
hiddenimports += collect_submodules('PIL')
hiddenimports += ['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 
                   'tkinter.messagebox', 'tkinter.scrolledtext']

# Analysis
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ (Python zip archive)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# EXE
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF_OCR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI application, no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico' if os.path.exists('app_icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)

# COLLECT (creates the distribution folder)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF_OCR',
)
