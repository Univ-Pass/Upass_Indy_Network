#!/bin/bash

# set -e

# name: docker container name
name="$1"
wallet_name="$2"
wallet_key="$3"

echo create wallet and did !!

echo "${wallet_name}"
echo "${wallet_key}"

# Get DID info with params & Export ouput file
docker exec -iu 0 "$name" python3 /home/indy/get_did.py "${wallet_name}" "${wallet_key}"

# Copy output file to Deploy folder
docker cp "$name":/home/indy/student_did.json /home/deploy
echo file copy !!

echo "<process end>"
