#!/bin/bash

APP_VERSION="1.0"
APP_NAME="personal-website-1"
CONTAINER_PORT=5000
HOST_PORT=5000

docker rm -f ${APP_NAME}-${APP_VERSION} 2>/dev/null || true

docker build -t ${APP_NAME}:${APP_VERSION} .

docker run -d \
  --name ${APP_NAME}-${APP_VERSION} \
  -p ${HOST_PORT}:${CONTAINER_PORT} \
  -v $(pwd)/output:/app/output \
  -v  $(pwd)/logs:/app/logs \
  ${APP_NAME}:${APP_VERSION}

docker image ls ${APP_NAME}

docker ps --filter "name=${APP_NAME}-${APP_VERSION}"
