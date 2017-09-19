#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
      ###########################################
      ## Metadata
      name="inscriptis",
      version="0.0.2.1",
      description='inscriptis - HTML to text converter.',
      author='Albert Weichselbraun, Fabian Odoni',
      author_email='albert.weichselbraun@htwchur.ch, fabian.odoni@htwchur.ch',
      url='http://github.com/weblyzard/inscriptis',
      license="GPL2",
      package_dir={'': 'src'},

      ###########################################
      ## Package List
      packages=find_packages('src'),

      ###########################################
      ## scripts
      scripts = [
        'scripts/inscript.py'
      ]

)
