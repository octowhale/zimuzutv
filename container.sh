#!/bin/bash

cd $(dirname $0)

IMAGE_VERSION=$(grep "ENV IMAGE_VERSION" Dockerfile | awk '{print $NF}')

function _build()
{
    git pull
    docker build -t zimuzutv:${IMAGE_VERSION} -f Dockerfile .
}

function _stop()
{
    docker container stop zimuzutv
    docker container rm zimuzutv
}

function _start()
{
    docker run -d --rm -p 23333:23333 --name zimuzutv --network zimuzu zimuzutv:${IMAGE_VERSION}
}

function _restart()
{
    _stop
    _start
}

case $1 in 
build)
    _build ;;
stop|start|restart)
    _${1} ;;
esac
