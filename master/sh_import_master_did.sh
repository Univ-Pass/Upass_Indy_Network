#!/bin/bash

# set -e

did="$1"
seed="$2"
wallet_name="$3"
wallet_key="$4"

new_wallet_command="${did}_master_wallet_command.txt"

# python3 export_master_did.py "${did}"
python3 export_master_did.py "${did}" "${seed}"

echo "<< Process Start >>\n"

# Write command file for indy-cli
echo "pool connect mainpool" >> "${new_wallet_command}"
echo "wallet create ""${wallet_name}" "key=""${wallet_key}" >> "${new_wallet_command}"
echo "wallet open ""${wallet_name}" "key=""${wallet_key}" >> "${new_wallet_command}"
echo "did import ./${did}Did.json" >> "${new_wallet_command}"
echo "wallet close " >> "${new_wallet_command}"
echo "exit" >> "${new_wallet_command}"


# Control indy-cli with command file
./indy-cli "${new_wallet_command}"

# docker exec -iu 0 "$name" rm /home/indy/"${seed}"NewWalletID.json
rm "${did}"Did.json
rm "${did}_master_wallet_command.txt"

echo "<< Process End >>\n"
