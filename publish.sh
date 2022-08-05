#!/bin/bash

# TODO
# - check release version number!

# publish the latest package to pypi
# sources:
# - https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project
# - https://packaging.python.org/guides/making-a-pypi-friendly-readme/

VERSION=$(grep -Po "\b__version__ = '\K[^']+" src/inscriptis/metadata.py)
IMAGE_NAME=inscriptis

case "$1" in
	python)
		# cleanup dist
		rm -rf ./dist

		# build and verify packages
		python3 setup.py sdist bdist_wheel; twine check dist/*

		# upload
		twine upload dist/*
		;;
	docker)
		echo "Publishing ${IMAGE_NAME} in version ${VERSION}"
		docker login ghcr.io -u AlbertWeichselbraun --password-stdin < ../github-token.txt
		docker build -t ${IMAGE_NAME}:${VERSION} .

		# Step 2: Tag
		docker tag ${IMAGE_NAME}:${VERSION} ghcr.io/weblyzard/${IMAGE_NAME}:${VERSION}
		docker tag ${IMAGE_NAME}:${VERSION} ghcr.io/weblyzard/${IMAGE_NAME}:latest

		# Step 3: Publish
		docker push ghcr.io/weblyzard/${IMAGE_NAME}:${VERSION}
		;;
esac
