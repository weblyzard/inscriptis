#!/usr/bin/env python

"""Inscriptis setup script."""

from pathlib import Path
from setuptools import setup, find_packages
from os import path


here = Path(path.dirname(__file__)).resolve()
# get version information
with here.joinpath('src/inscriptis/metadata.py').open() as f:
    exec(f.read())

# Get the long description from the README.md file
with here.joinpath('README.rst').open() as f:  # , encoding='utf-8'
    long_description = f.read()

setup(
    # Metadata
    name='inscriptis',
    version=__version__,
    description='inscriptis - HTML to text converter.',
    long_description=long_description,
    author=__author__,
    author_email=__author_email__,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='HTML,converter,text',
    url='https://github.com/weblyzard/inscriptis',
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
    ],
)
