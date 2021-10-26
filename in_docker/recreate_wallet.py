import asyncio
from collections import OrderedDict
import json
import pprint
import sys
import re

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION, add_error, print_log, POOL_NAME

pool_name = POOL_NAME
genesis_file_path = get_pool_genesis_txn_path(pool_name)

user_data = OrderedDict()

# User E-Mail Address
wallet_name = sys.argv[1]
wallet_key = sys.argv[2]
wallet_new_key = sys.argv[3]

# User DID's Seed
student_seed = sys.argv[4]

file_name = wallet_name + "Did.json"

wallet_config = json.dumps({"id": wallet_name})
wallet_credentials = json.dumps({"key": wallet_key})
wallet_new_credentials = json.dumps({"key": wallet_new_key})


async def create_did_and_write_nym():
    try:
        await pool.set_protocol_version(PROTOCOL_VERSION)

        print_log('genesis_txn: ', genesis_file_path)

        # 1.
        print_log('\n1. Open pool ledger and get handle from libindy\n')
        pool_handle = await pool.open_pool_ledger(config_name=pool_name, config=None)

        # 2.
        print_log('\n2. Open previous wallet and get handle from libindy\n')
        wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

        # 3.
        print_log('\n3. List my DID\n')
        my_did = await did.list_my_dids_with_meta(wallet_handle)
        list_did = my_did.split("},{")

        #4.
        print_log('\n4. Parse DID \n')
        for i in list_did:
            if "StudentID" in i:
                i = re.sub("\[|\'|\]","", i)
                if i.count("{") != 1:
                    i = "{" + i
                elif i.count("}") != 1:
                    i = i + "}"
                jsonObject = json.loads(i)
                student_DID = jsonObject.get("did")
                print_log("Student DID: " + student_DID)

        
        # 5.
        print_log('\n5. Set metadata \n')
        did_seed = "0000000000000000STUDENT" + student_seed
        result = {}
        result['version'] = 1
        result['dids'] = []
        _did = {}
        _did['did'] = student_DID
        _did['seed'] = did_seed

        result['dids'].append(_did)

        print_log('\n5. Export DID \n')

        # Export json of DID file
        with open(file_name,'w',encoding="utf-8") as make_file:
            json.dump(result, make_file, ensure_ascii=False, indent="\t")

        print_log('\nExport DID Success!! \n')

        # 6.
        print_log('\n6. Closing wallet and pool\n')
        await wallet.close_wallet(wallet_handle)
        await pool.close_pool_ledger(pool_handle)

        # 7.
        print_log('\n7. Deleting created wallet\n')
        await wallet.delete_wallet(wallet_config, wallet_credentials)

        #8.
        print_log('\n8. Creating new secure wallet\n')
        try:
            await wallet.create_wallet(wallet_config, wallet_new_credentials)
        except IndyError as ex:
            if ex.error_code == ErrorCode.WalletAlreadyExistsError:
                pass
        
        print_log('\n[End of Process]\n')

    except IndyError as e:
        add_error(file_name)
        print('Error occurred: %s' %e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_did_and_write_nym())
    loop.close()


if __name__ == '__main__':
    main()
