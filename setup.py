#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from sys import exit

setup(
      ###########################################
      ## Metadata
      name="inscriptis",
      version="0.0.1",
      description='inscriptis - HTML to text converter.',
      author='Fabian Odoni, Albert Weichselbraun, Samuel Abels',
      author_email='fabian.odoni@htwchur.ch, albert.weichselbraun@htwchur.ch, samuel.abels@debain.org',
      url='http://github.com/weblyzard/inscriptis',
      license="GPL2",
      package_dir={'': 'src'},

      ###########################################
      ## Package List
      packages = find_packages('src'),

)
