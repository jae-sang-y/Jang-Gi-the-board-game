import shutil

import setuptools as setuptools
from setuptools.extension import Extension

try:
    shutil.rmtree('build')
except FileNotFoundError:
    pass

setuptools.setup(
    name='jangi_extension',
    ext_modules=[
        Extension(
            name='jangi_extension',
            sources=['jangi_extension.cpp'],
            include_dirs=['../dataset'],
            library_dirs=['../lib'],
            libraries=['actor'],
            language='c++',
        )
    ]
)
