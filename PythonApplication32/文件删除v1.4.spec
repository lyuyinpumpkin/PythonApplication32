# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:\\Users\\FESL14A835\\source\\repos\\PythonApplication32\\PythonApplication32\\文件删除v1.4.py'],
             pathex=['C:\\Users\\FESL14A835\\source\\repos\\PythonApplication32\\PythonApplication32'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='文件删除v1.4',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\FESL14A835\\source\\repos\\PythonApplication32\\PythonApplication32\\delete_folder_128px_1232010_easyicon.net.ico')
