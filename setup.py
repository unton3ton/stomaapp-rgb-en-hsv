# coding: utf-8

# python setup.py build

from cx_Freeze import setup, Executable

executables = [Executable('app4Stoma.py')]

options = {
    'build_exe': {
        'include_msvcr': True,
    }
}

setup(name='stomaapp',
      version='0.2.1',
      description='MyApp',
      executables=executables,
      options=options)