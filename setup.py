#!/usr/bin/env python

from setuptools import setup

setup(name='LazyTools',
      packagez=['LazyTools'],
      version='0.1.0',
      description='Useful python modules for lazy scripting.',
      author='James Wenzel',
      author_email='wenzel.james.r@gmail.com',
      url='https://github.com/jameswenzel/LazyTools',
      download_url='https://github.com/jameswenzel/LazyTools/tarball/0.1.0',
      license='Apache License, Version 2.0',
      keywords=['lazy', 'csv', 'tor', 'multithread', 'beautifulsoup', 'json'],
      classifiers=[],
      install_requires=['beautifulsoup4 >= 4.4.1', 'requests >= 2.2.1',
                        'stem >= 1.4']
      )