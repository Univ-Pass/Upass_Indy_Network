#!/bin/bash

set -e

name="$1"
wallet_name="$2"
wallet_key="$3"

echo create wallet and did !!

echo "${wallet_name}"
echo "${wallet_key}"

docker exec -iu 0 "$name" python3 /home/indy/get_did.py "${wallet_name}" "${wallet_key}"

echo file copy !!
docker cp "$name":/home/indy/student_did.json /home/deploy

echo "<process end>"
