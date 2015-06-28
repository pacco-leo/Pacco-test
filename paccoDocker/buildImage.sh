#!/bin/sh

export IMAGE="paccotest"
export VERSION="latest"

echo "Remove untagged versions"
./removeUntaggedVersions.sh 
echo "Removing previous Images of ${IMAGE}"
docker rmi -f ${IMAGE}

#docker build -t ${IMAGE} .
docker build -t ${IMAGE}:${VERSION} .
docker tag -f ${IMAGE}:${VERSION} ${IMAGE}:latest
