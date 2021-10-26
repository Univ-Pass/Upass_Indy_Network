#!/bin/bash

# set -e

# name: docker container name
name="$1"
wallet_name="$2"
wallet_key="$3"
new_key="$4"
seed="$5"

import_did="${wallet_name}_import_did.txt"

echo "<< Process Start >>\n"

# Import DID to new wallet with params & Export ouput file
docker exec -iu 0 "${name}" python3 /home/indy/import_did.py "${wallet_name}" "${wallet_key}" "${new_key}" "${seed}"

# Write command file for indy-cli
echo "pool connect testpool"
echo "wallet attach" "${wallet_name}" >> "${import_did}"
echo "wallet open ""${wallet_name}" "key=""${new_key}" >> "${import_did}"
echo "did import /home/indy/${wallet_name}ImportDid.json" >> "${import_did}"
echo "exit" >> "${import_did}"

# Copy output file to docker container
docker cp ./"${import_did}" "${name}":/home/indy

# Control indy-cli with command file
docker exec -iu 0 "${name}" indy-cli /home/indy/"${import_did}"

rm "${import_did}"

echo "<< Process End >>\n"
