import os
from distutils.core import setup, Extension

os.system('rmdir /S /Q build')
module1 = Extension(
    'board_in_c',
    include_dirs=[
        r'C:\Users\YJS-ATX\AppData\Local\Programs\Python\Python39\include',
        r'C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt',
        r'C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include',
        r'C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared'

    ],
    extra_compile_args=['-std:c++20'],
    library_dirs=[
        r'C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\lib\x64',
        r'C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\um\x64',
        r'C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\ucrt\x64',
        r'C:\Users\YJS-ATX\AppData\Local\Programs\Python\Python39\libs'

    ],
    sources=['board_in_c.cpp']
)
setup(
    name='BoardInC',
    ext_modules=[module1]
)
