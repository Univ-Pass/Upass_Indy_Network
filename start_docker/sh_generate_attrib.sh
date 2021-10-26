#!/bin/bash

# set -e

# name: docker container name
name="$1"
wallet_name="$2"
wallet_key="$3"
admin_did="$4"
user_did="$5"

building="$6"
year="$7"
month="$8"
day="$9"

echo "<< Process Start >>\n"

echo "[open wallet]"

echo "\twallet_name: ${wallet_name}"
echo "\twallet_key: ${wallet_key}"

# Generate Attrib with params & Export ouput file
docker exec -iu 0 "$name" python3 /home/indy/generate_attrib.py "${wallet_name}" "${wallet_key}" "${admin_did}" "${user_did}" "${building}" "${year}" "${month}" "${day}"

# Copy output file to docker container
docker cp "$name":/home/indy/"${wallet_name}"_gen_attrib.json /home/deploy
# docker cp "$name":/home/indy/"${wallet_name}"_gen_attrib.json ./
echo "[Log File Copy Docker to Server]"

docker exec -iu 0 "$name" rm /home/indy/"${wallet_name}"_gen_attrib.json

echo "[Log File Remove From 'Docker']"

echo "<< Process End >>\n"
