# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/home/pi/Desktop/new_attendance/main.py'],
             pathex=['/home/pi/Desktop/face_new'],
             binaries=[],
             datas=[],
             hiddenimports=['tensorflow_core', 'pkg_resources.py2_warn', 'google-api-python-client', 'apiclient', 'pyautogui', 'google-api-core', 'google-auth', 'googleapiclient', 'PIL._tkinter_finder'],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
