from distutils.core import setup, Extension
cgamestate = Extension('csocha', sources=['socha/csocha.cpp'])
setup(name='csocha', ext_modules=[cgamestate])
