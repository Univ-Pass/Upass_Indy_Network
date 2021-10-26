#!/bin/bash

set -e

echo "<< Process Start >>\n"

IMAGE_NAME="$1" # docker image name or ID

sudo docker run -tid "$IMAGE_NAME" sh ./init.sh # start docker with image name and run sh file

CONTAINER_ID=$(sudo docker run -tid "$IMAGE_NAME" /bin/bash)
docker exec -itu 0 "$CONTAINER_ID" sh /home/indy/init.sh

echo "<< Process End >>\n"
