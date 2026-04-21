# -*- mode: python ; coding: utf-8 -*-
import sys
import os

IS_MAC = sys.platform == 'darwin'
IS_WINDOWS = sys.platform.startswith('win')

icon_file = 'icon.icns' if (IS_MAC and os.path.exists('icon.icns')) else \
            ('icon.ico' if (IS_WINDOWS and os.path.exists('icon.ico')) else 'icon.png')

datas = [('ui', 'ui')]
if os.path.exists('web/dist'):
    datas.append(('web/dist', 'web/dist'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets',
        'PyQt6.QtWebEngineWidgets', 'PyQt6.QtWebChannel',
        'sqlite3', 'asyncio', 'threading',
    ],
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
    name='TASKY',
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
    icon=[icon_file],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TASKY',
)

if IS_MAC:
    app = BUNDLE(
        coll,
        name='TASKY.app',
        icon='icon.icns' if os.path.exists('icon.icns') else None,
        bundle_identifier='com.tasky.app',
        info_plist={
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.14',
            'CFBundleShortVersionString': '2.0.0',
            'CFBundleVersion': '2.0.0',
            'NSRequiresAquaSystemAppearance': False,
        },
    )
