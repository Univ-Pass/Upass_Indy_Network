#! /bin/bash

# set -e

# name: docker container name
name="$1"
admin_did="$2"
user_did="$3"
year="$4"
month="$5"

echo "<< Process Start >>\n"

# Get Attrib info with params & Export ouput file
docker exec -iu 0 "$name" python3 /home/indy/get_attrib.py "${admin_did}" "${user_did}" "${year}" "${month}"

# Copy output file to Deploy folder
docker cp "$name":/home/indy/"${user_did}"_attrib.json /home/deploy
echo "[Copy log file from Docker to Server]"

docker exec -iu 0 "$name" rm /home/indy/"${user_did}"_attrib.json
echo "[Remove log file from 'Docker']"

echo "<< Process End >>\n"