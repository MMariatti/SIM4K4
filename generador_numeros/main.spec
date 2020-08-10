# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=[''],
             binaries=[],
             datas=[('./interfaz/*.ui', './interfaz')],
             hiddenimports=['reportlab.graphics.barcode.common',
                            'reportlab.graphics.barcode.code128',
                            'reportlab.graphics.barcode.code93',
                            'reportlab.graphics.barcode.code39',
                            'reportlab.graphics.barcode.code93',
                            'reportlab.graphics.barcode.usps',
                            'reportlab.graphics.barcode.usps4s',
                            'reportlab.graphics.barcode.ecc200datamatrix'
                            'numpy.random.common',
                            'numpy.random.bounded_integers'
                            'numpy.random.entropy'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)
