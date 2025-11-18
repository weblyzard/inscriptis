#!/bin/bash

# Publishing sequence:
# ====================
# 1. create pypi package
# 2. publish docker container
# 3. create github release (which runs the helm scripts)

# publish the latest package to pypi
# sources:
# - https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project
# - https://packaging.python.org/guides/making-a-pypi-friendly-readme/

VERSION=$(grep -oP '^version = "\K[^"]+' pyproject.toml)
IMAGE_NAME=inscriptis

case "$1" in
	python)
		# cleanup dist
		rm -rf ./dist

		# build with hatchling and publish to PyPI
		uv build
		uv publish
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
