#!/bin/bash

# set -e

# name: docker container name
name="$1"
did="$2"
seed="$3"
email="$4"
wallet_name="$5"
wallet_key="$6"

new_wallet_command="${wallet_name}_new_wallet_command.txt"

echo "<< Process Start >>\n"

# Export did with params & Export ouput file
docker exec -iu 0 "${name}" python3 /home/indy/export_did.py "${did}" "${seed}"

# Write command file for indy-cli
echo "pool connect mainpool" >> "${new_wallet_command}"
echo "wallet create ""${wallet_name}" "key=""${wallet_key}" >> "${new_wallet_command}"
echo "wallet open ""${wallet_name}" "key=""${wallet_key}" >> "${new_wallet_command}"
echo "did import /home/indy/${seed}Did.json" >> "${new_wallet_command}"
echo "wallet close " >> "${new_wallet_command}"
echo "wallet detach" "${wallet_name}" >> "${new_wallet_command}"
echo "exit" >> "${new_wallet_command}"

# Copy output file to docker container
docker cp ./"${new_wallet_command}" "${name}":/home/indy

# Control indy-cli with command file
docker exec -iu 0 "${name}" indy-cli /home/indy/"${new_wallet_command}"

# Set metadata with params
docker exec -iu 0 "${name}" python3 /home/indy/set_metadata.py "${wallet_name}" "${wallet_key}"

# Export new wallet id & Export output file
docker exec -iu 0 "${name}" python3 /home/indy/export_wallet_id.py "${email}" "${wallet_name}" "${seed}"

rm "${new_wallet_command}"

# Copy output file to Deploy folder
docker cp "$name":/home/indy/"${seed}"NewWalletID.json /home/deploy
echo "[Copy log file from Docker to Server]"

docker exec -iu 0 "$name" rm /home/indy/"${seed}"NewWalletID.json
docker exec -iu 0 "$name" rm /home/indy/"${seed}"Did.json
echo "[Remove log file from 'Docker']"

echo "<< Process End >>\n"
