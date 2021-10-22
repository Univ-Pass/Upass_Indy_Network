#!/bin/bash

set -e

echo "<< Process Start >>\n"

IMAGE_NAME="$1" # docker image name or ID
git_email="$2"
git_passwd="$3"

CONTAINER_ID=$(sudo docker run -tid "$IMAGE_NAME" /bin/bash)

docker cp ./make_pool.txt "$CONTAINER_ID":/home/indy/
docker cp ./genesis "$CONTAINER_ID":/home/indy/

docker exec -itu 0 "$CONTAINER_ID" indy-cli /home/indy/make_pool.txt
# docker exec -iu 0 "$CONTAINER_ID" git init /home/indy/
# docker exec -iu 0 "$CONTAINER_ID" git config core.sparseCheckout true
# docker exec -iu 0 "$CONTAINER_ID" echo "in_docker" >> /home/indy/.git/info/sparse-checkout
docker exec -iu 0 "$CONTAINER_ID" git pull https://"$git_email":"$git_passwd"@github.com/Univ-Pass/Upass_Indy_Network.git
docker exec -iu 0 "$CONTAINER_ID" cp -r /home/indy/in_docker/. /home/indy/

echo "<< Process End >>\n"
