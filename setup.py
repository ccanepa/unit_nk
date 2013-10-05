#!/usr/bin/env python

# find_package data is
# (c) 2005 Ian Bicking and contributors; written for Paste
# (http://pythonpaste.org)
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license.php

# Don't use __future__ in this script, it breaks buildout
# from __future__ import print_function
import os
import subprocess
import sys
import shutil
from fnmatch import fnmatchcase


try:
    # Prefer setuptools for the installation to have no problem with the
    # "--single-version-externally-managed" option that pip uses when
    # installing packages.
    from setuptools import setup
    from setuptools import convert_path

    from setuptools.command.install import install
except ImportError:
    print('\n*** setuptools not found! Falling back to distutils\n\n')
    from distutils.core import setup  # NOQA

    from distutils.command.install import install
    from distutils.util import convert_path  # NOQA

with open('requirements.txt', 'r') as fh:
    dependencies = [l.strip() for l in fh]

class k_install(install):
    def run(self):
        install.run(self)


setup(name='unit_nk',
      version='6.0.4',
      description='testing nikola',
      long_description='long desc',
      author='cc',
      author_email='ralsina@netmanagers.com.ar',
      url='http://getnikola.com',
      packages = ['unit_nk'],
      license='MIT',
      keywords='website, static',
      classifiers=('Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Environment :: Plugins',
                   'Environment :: Web Environment',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: OS Independent',
                   'Operating System :: POSIX',
                   'Operating System :: Unix',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Internet',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Text Processing :: Markup'),
      install_requires=dependencies,
      cmdclass={'install': k_install},
      zip_safe = False,
      )
