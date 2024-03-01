from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.


build_options = {'packages': [],
                 'excludes': []}

if sys.platform == 'win32':

    executables = [
        Executable('tk/main.py',
                   base='Win32GUI',
                   target_name='tksteg',
                   icon="tk/tksteg.ico",
                   # shortcutDir="DesktopFolder",
                   # shortcutName="TkSteg",
                   ),
        Executable('cli/csteg.py', base=None, target_name='csteg')
    ]

    setup(name='steg',
          version='1.0',
          description='Simple steganography',
          options={'build_exe': build_options},
          executables=executables)
elif sys.platform == 'linux':
    print("""To build a single file exe @ linux, use rather:
   $ pyinstaller tksteg.spec
or single line command:
   $ pyinstaller main.py --hiddenimport PIL --hiddenimport PIL._imagingtk
     --hiddenimport PIL._tkinter_finder --name tksteg""")
else:
    print("Only win and linux supported at the moment")
