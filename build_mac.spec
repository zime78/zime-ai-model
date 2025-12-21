# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Hidden imports required for commonly used libraries
hidden_imports = [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'pydantic.deprecated.decorator', # Sometimes needed
    'tiktoken_ext.openai_public',
    'tiktoken_ext',
]

a = Analysis(
    ['apps/server/bundle_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('apps/web/out', 'static'),  # Embed frontend assets
        ('.env.example', '.'),       # Include example env
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyBrainAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # Windowed mode for App Bundle
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='MyBrainAI.app',
    icon=None,
    bundle_identifier='com.zime.mybrainai',
    info_plist={
        'NSHighResolutionCapable': True,
        'LSBackgroundOnly': False,
        'CFBundleDisplayName': 'MyBrainAI',
        'CFBundleName': 'MyBrainAI',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
    },
)
