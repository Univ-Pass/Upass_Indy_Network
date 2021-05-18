#! /bin/bash

# set -e

# name: docker container name
name="$1"
wallet_name="$2"
wallet_key="$3"
did="$4"

year="$5"
month="$6"
day="$7"

echo "[open wallet]"

echo "\twallet_name: ${wallet_name}"
echo "\twallet_key: ${wallet_key}"

docker exec -iu 0 "$name" python3 /home/indy/get_attrib.py "${wallet_name}" "${wallet_key}" "${did}" "${year}" "${month}" "${day}"

docker cp "$name":/home/indy/attrib.json /home/deploy

echo "<< Process End >>"