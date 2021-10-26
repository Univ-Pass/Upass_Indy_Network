#!/bin/bash

git_email="$1"
git_passwd="$2"

docker_list="3cb6b47ad897 e39de3ebf718" # 도커 컨테이너 ID 입력해주세요

echo "<< Process Start >>\n"

for var in $docker_list
do
    docker exec -iu 0 $var git pull https://"$git_email":"$git_passwd"@github.com/beenee010/Blockchain_Capstone_Indy.git
    docker exec -iu 0 $var cp -r * /home/indy/in_docker/ /home/indy/
    echo "[Success: git pull]\n"
done

echo "<< Process End >>\n"
