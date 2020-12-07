#!/bin/bash

# TODO
# - check release version number!

# publish the latest package to pypi
# sources:
# - https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project
# - https://packaging.python.org/guides/making-a-pypi-friendly-readme/

VERSION=$(grep -Po "\b__version__ = '\K[^']+" src/inscriptis/__init__.py)
IMAGE_NAME=inscriptis-web-service

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
		docker login docker.pkg.github.com -u AlbertWeichselbraun --password-stdin < ../github-token.txt
		docker build -t ${IMAGE_NAME}:${VERSION} .

		# Step 2: Tag
		docker tag ${IMAGE_NAME}:${VERSION} docker.pkg.github.com/weblyzard/inscriptis/${IMAGE_NAME}:${VERSION}

		# Step 3: Publish
		#docker push docker.pkg.github.com/weblyzard/inscriptis/${IMAGE_NAME}:${VERSION}
		;;
esac
