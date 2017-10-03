#!/bin/bash

cd $(dirname $0)

git pull

IMAGE_VERSION=$(grep "ENV IMAGE_VERSION" Dockerfile | awk '{print $NF}')

docker build -t zimuzutv:${IMAGE_VERSION} -f Dockerfile .

docker container stop zimuzutv
docker container rm zimuzutv
docker run --rm -p 23333:23333 --network zimuzu zimuzutv:${IMAGE_VERSION}
