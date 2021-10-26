import asyncio
import json
import pprint
import sys
import re

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION, add_error, print_log, POOL_NAME

pool_name = POOL_NAME
genesis_file_path = get_pool_genesis_txn_path(pool_name)

wallet_name = sys.argv[1]
wallet_key = sys.argv[2]

wallet_config = json.dumps({"id": wallet_name})
wallet_credentials = json.dumps({"key": wallet_key})

def print_log(value_color="", value_noncolor=""):
    """set the colors for text."""
    HEADER = '\033[92m'
    ENDC = '\033[0m'
    print(HEADER + value_color + ENDC + str(value_noncolor))


async def write_nym_and_query_verkey():
    try:
        await pool.set_protocol_version(PROTOCOL_VERSION)

        # 1.
        print_log('\n1. Open pool ledger and get handle from libindy\n')
        await pool.open_pool_ledger(config_name=pool_name, config=None)
        
        # 2.
        print_log('\n2. Open wallet and get handle from libindy\n')
        wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

        #3.
        print_log('\n3. List my DID\n')
        my_did = await did.list_my_dids_with_meta(wallet_handle)
        my_did = re.sub("\[|\'|\]","",my_did)

        json_did = my_did
        jsonObject = json.loads(json_did)
        student_did = jsonObject.get("did")
        print_log(student_did)

        # 4.
        print_log('\n4. Set DID\'s Meta data of new Wallet\n')
        await did.set_did_metadata(wallet_handle, student_did, "StudentID")

        #5.
        print_log('\n5. Generating and storing steward DID and verkey\n')
        steward_seed = '000000000000000000000000Steward1'
        did_json = json.dumps({'seed': steward_seed})
        steward_did, steward_verkey = await did.create_and_store_my_did(wallet_handle, did_json)
        print_log('Steward DID: ', steward_did)
        print_log('Steward Verkey: ', steward_verkey)
        
        # Set Steward DID's metadata
        await did.set_did_metadata(wallet_handle, steward_did, "Steward")

        print_log('\n[End of Process]\n')
        
    except IndyError as e:
        print('Error occurred: %s' % e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(write_nym_and_query_verkey())
    loop.close()


if __name__ == '__main__':
    main()


