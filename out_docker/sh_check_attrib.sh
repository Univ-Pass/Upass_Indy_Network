#!/bin/bash

# set -e

# name: docker container name
name="$1"
admin_did="$2"
info_hash="$3"
student_id="$4"

echo "<< Process Start >>\n"

# Check Attrib with params & Export ouput file
docker exec -iu 0 "$name" python3 /home/indy/check_attrib.py "${admin_did}" "${info_hash}" "${student_id}"

# Copy output file to docker container
docker cp "$name":/home/indy/"${student_id}"_check_attrib.json /home/deploy
# docker cp "$name":/home/indy/"${student_id}"_check_attrib.json ./
echo "[Log File Copy Docker to Server]"

# echo "[Log File Remove From 'Docker']"
docker exec -iu 0 "${name}" rm /home/indy/"${student_id}"_check_attrib.json

echo "<< Process End >>\n"
