#!/bin/bash

# TODO
# - check release version number!

# publish the latest package to pypi
# sources:
# - https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project
# - https://packaging.python.org/guides/making-a-pypi-friendly-readme/

# cleanup dist
rm -rf ./dist

# build and verify packages
python3 setup.py sdist bdist_wheel; twine check dist/*

# upload
twine upload dist/*
