from distutils.core import setup, Extension

setup(name='nettoolbox',
      version='1.0',
      ext_modules=[Extension('nettoolbox', ['nettoolbox.c'])])
