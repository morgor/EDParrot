
a = Analysis(['edparrot.py'],
             pathex=['C:\\Users\\jackm\\Documents\\Blog Posts\\Gooey_Inno\\.env\\Scripts'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             )
pyz = PYZ(a.pure)

options = [('u', None, 'OPTION')]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          options,
          name='main',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon=os.path.join('gfx', 'program_ikona.ico'))