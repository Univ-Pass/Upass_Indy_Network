#!/bin/bash

# set -e

# name: docker container name
name="$1"
wallet_name="$2"
wallet_key="$3"
new_key="$4"
seed="$5"

attach_command="${wallet_name}_attath_command.txt"
did_import_command="${wallet_name}_did_import_command.txt"

echo "<< Process Start >>\n"

# Wallet Attach
echo "pool connect testpool" >> "${attach_command}"
echo "wallet attach" "${wallet_name}" >> "${attach_command}"
echo "exit" >> "${attach_command}"

docker cp ./"${attach_command}" "${name}":/home/indy
docker exec -iu 0 "${name}" indy-cli /home/indy/"${attach_command}"

# Recreate Wallet with params & Export ouput file
docker exec -iu 0 "${name}" python3 /home/indy/recreate_wallet.py "${wallet_name}" "${wallet_key}" "${new_key}" "${seed}"

# # Write command file for indy-cli
echo "pool connect testpool" >> "${did_import_command}"
echo "wallet open ""${wallet_name}" "key=""${new_key}" >> "${did_import_command}"
echo "did import /home/indy/${wallet_name}Did.json" >> "${did_import_command}"
echo "wallet close " >> "${did_import_command}"
echo "wallet detach" "${wallet_name}" >> "${did_import_command}"
echo "exit" >> "${did_import_command}"

# Copy output file to docker container
docker cp ./"${did_import_command}" "${name}":/home/indy

echo "[Log File Copy]"

# Control indy-cli with command file
docker exec -iu 0 "${name}" indy-cli /home/indy/"${did_import_command}"

# set metadata
docker exec -iu 0 "${name}" python3 /home/indy/set_metadata.py "${wallet_name}" "${new_key}"

docker exec -iu 0 "${name}" rm ${wallet_name}Did.json
echo "[Remove log file from 'Docker']"

# remove log file
rm "${did_import_command}"
rm "${attach_command}"
echo "[Remove log file from 'Server']"

echo "<< Process End >>\n"
