# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['EditorKML_v2_2.py', 'Ajuda.py', 'Display.py', 'FinestraRutes.py', 'FinPpal.py', 'Rutes.py'],
             pathex=['C:\\Users\\Jordi\\Desktop\\EditorKML'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='EditorKML_v2_2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='EditorKML_v2_2')
