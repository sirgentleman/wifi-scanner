from distutils.core import setup, Extension

setup(
    name='net_scanner',
    version='1.0',
    description='Network scanning utility.',
    author='Błażej Ułanowicz',
    license='Unlicense',
    packages=['net_scanner', 'net_scanner.mail', 'net_scanner.networking'],
    ext_modules=[Extension('nettoolbox', ['net_scanner/networking/nettoolbox.c'])])
