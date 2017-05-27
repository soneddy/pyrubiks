#!/usr/bin/env python

"""
N x N x N Rubik's Cube
"""

from distutils.core import setup
from python import __author__, __version__, __date__

setup(name='pyrubiks',
      version=__version__,
      description="N x N x N Rubik's Cube",
      author='Edwin J. Son',
      author_email='edwin.son@ligo.org',
      url='https://github.com/soneddy/pyrubiks',
      packages=['pyrubiks'],
      package_dir={'pyrubiks': 'python'},
     )
