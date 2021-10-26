import asyncio
from collections import OrderedDict
import json
import pprint
import sys
import datetime
import hashlib

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION, add_error, print_log, POOL_NAME

steward_did = 'Th7MpTaRZVRYnPiabds81Y'
genesis_file_path = get_pool_genesis_txn_path(POOL_NAME)

user_data = OrderedDict()

# Params
wallet_name = sys.argv[1]
wallet_key = sys.argv[2]

# DID of Building manager
master_did = sys.argv[3]

student_id = sys.argv[4]
dept = sys.argv[5]
email_id = sys.argv[6]

email = email_id + '@kyonggi.ac.kr'

info = student_id + dept + email
info_hash = hashlib.sha256(info.encode('utf-8')).hexdigest()

file_name = student_id + "_info_hash_data.json"

wallet_config = json.dumps({"id": wallet_name})
wallet_credentials = json.dumps({"key": wallet_key})


async def generate_attrib_transaction():
    try:
        await pool.set_protocol_version(PROTOCOL_VERSION)

        print_log('genesis_txn: ', genesis_file_path)

        # 1.
        print_log('\n1. Open pool ledger and get handle from libindy\n')
        pool_handle = await pool.open_pool_ledger(config_name=POOL_NAME, config=None)

        # 2.
        print_log('\n2. Open wallet and get handle from libindy\n')
        wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

        #3.
        print_log('\n3. Get DID and Verkey From wallet\n')
        did_result = await did.get_my_did_with_meta(wallet_handle, master_did)
        
        # 4.
        print_log('\n4. Generate Attrib Transaction\n')
        
        # Save Transactions log
        
        attrib_transaction_request = await ledger.build_attrib_request(master_did, master_did,None, 
        '{"'+info_hash + '":{"info_hash": "' + info_hash  + '"}}', None)

        attrib_transaction_response = await ledger.sign_and_submit_request(pool_handle=pool_handle,
                                                                        wallet_handle=wallet_handle,
                                                                        submitter_did=master_did,
                                                                        request_json=attrib_transaction_request)
        print_log(attrib_transaction_response)

        # Set value of json
        json_data = {}
        json_data['error'] = "None"
        json_data['info_hash'] = info_hash

        # Export json of Tx info
        with open(file_name,'w',encoding="utf-8") as make_file:
            json.dump(json_data, make_file, ensure_ascii=False,indent="\t")

        print_log('\n[End of Process]\n')

    except IndyError as e:
        add_error(file_name)
        print('Error occurred: %s' %e)


def main():
    answer = input('\033[31m'+'<<<WARNING!!! THIS IS MAINPOOL!!! ARE YOU SURE? [y/N]>>> '+'\033[0m')
    if answer=='y' or answer=='Y' or answer=='yes':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(generate_attrib_transaction())
        loop.close()
    else:
        print('<<<PROCESS STOP>>>')


if __name__ == '__main__':
    main()

