#!/bin/bash

# email=""
# passwd=""

docker_list="7d79dbce62c6 0f317446d48b" # 도커 컨테이너 ID 입력해주세요

echo "<< Process Start >>\n"

# for var in $docker_list
# do
#     docker exec -iu 0 $var git push 

for var in $docker_list
do
    # docker exec -iu 0 $var rm /home/indy/*
    docker cp /home/caps/indy/in_docker/ "$var":/home/indy/
    echo "[Python File Copied]"
done
# Copy output file to Deploy folder

echo "<< Process End >>\n"