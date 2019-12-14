#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

init = open('src/inscriptis/__init__.py').read()
(__version__, ) = re.findall("__version__.*\s*=\s*[']([^']+)[']", init)
(__author__, ) = re.findall("__author__.*\s*=\s*[']([^']+)[']", init)
(__author_email__, ) = re.findall("__author_email__.*\s*=\s*[']([^']+)[']", init)
(__author_email__, ) = re.findall("__author_email__.*\s*=\s*[']([^']+)[']", init)
(__license__, ) = re.findall("__license__.*\s*=\s*[']([^']+)[']", init)

here = path.abspath(path.dirname(__file__))

# Get the long description from the README.md file
with open(path.join(here, 'README.md')) as f:  # , encoding='utf-8'
    long_description = f.read()

setup(
    # Metadata
    name="inscriptis",
    version=__version__,
    description='inscriptis - HTML to text converter.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=__author__,
    author_email=__author_email__,
    classifiers=[
           'Development Status :: 4 - Beta',
           'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
           'Topic :: Text Processing',
           'Topic :: Text Processing :: Markup :: HTML',
           'Programming Language :: Python :: 3',
           'Programming Language :: Python :: 3.5',
           'Programming Language :: Python :: 3.6',
           'Programming Language :: Python :: 3.7',
           'Programming Language :: Python :: 3.8',
    ],
    url='http://github.com/weblyzard/inscriptis',
    license=__license__,
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
