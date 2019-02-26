#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README.md file
with open(path.join(here, 'README.md')) as f:  # , encoding='utf-8'
    long_description = f.read()

setup(
    # Metadata
    name="inscriptis",
    version="0.0.4.0",
    description='inscriptis - HTML to text converter.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Albert Weichselbraun, Fabian Odoni',
    author_email='albert.weichselbraun@htwchur.ch, fabian.odoni@htwchur.ch',
    classifiers=[
           'Topic :: Text Processing :: Markup :: HTML',
           'Programming Language :: Python :: 3',
    ],
    url='http://github.com/weblyzard/inscriptis',
    license="GPL2",
    package_dir={'': 'src'},

    # Package List
    packages=find_packages('src'),

    # Scripts
    scripts=[
        'scripts/inscript.py'
    ],

    # Requirements
    install_requires=[
        'lxml',
        'requests'
    ]

)
