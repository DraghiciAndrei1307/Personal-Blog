#!/bin/bash

APP_VERSION="1.0"
APP_NAME="personal-website-1"
HOST_OUTPUT="/home/student/my_docker/personal-website-1/output"
HOST_LOGS="/home/student/my_docker/personal-website-1/logs"
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
