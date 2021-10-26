import asyncio
import json
import pprint
import sys
import re

from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode

from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION, add_error, print_log, POOL_NAME
from collections import OrderedDict

pool_name = POOL_NAME
genesis_file_path = get_pool_genesis_txn_path(pool_name)

# Params
wallet_name = sys.argv[1]
wallet_key = sys.argv[2]
file_name = str(wallet_name) + '_student_did.json'

wallet_config = json.dumps({"id": wallet_name})
wallet_credentials = json.dumps({"key": wallet_key})


async def get_did():
    try:
        await pool.set_protocol_version(PROTOCOL_VERSION)

        #1.
        print_log('\n1. Creates a new local pool ledger configuration that is used '
                  'later when connecting to ledger.\n')
        pool_config = json.dumps({'genesis_txn': str(genesis_file_path)})

        try:
            await pool.create_pool_ledger_config(config_name=pool_name, config=pool_config)
        except IndyError as ex:
            add_error(file_name)
            if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
                pass
        
        #2.
        print_log('\n2. Open pool ledger and get handle from libindy\n')
        pool_handle = await pool.open_pool_ledger(config_name=pool_name, config=None)
                
        #3.
        print_log('\n3. Open wallet and get handle from libindy\n')
        wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

        #4.
        print_log('\n4. List my DID\n')
        my_did = await did.list_my_dids_with_meta(wallet_handle)
        list_did = my_did.split("},{")

        #5.
        print_log('\n5. Parse DID and Make "student_did.json" File\n')
        for i in list_did:
            print(i + "\n\n")
            if "StudentID" in i:
                i = re.sub("\[|\'|\]","", i)
                if i.count("{") != 1:
                    i = "{" + i
                elif i.count("}") != 1:
                    i = i + "}"
                print_log(i)
                jsonObject = json.loads(i)
                student_DID = jsonObject.get("did")
                print_log("Student DID: " + student_DID)
                # Export json of Student DID info
                with open(file_name,'w',encoding="utf-8") as make_file:
                    jsonObject['verkey'] = "None"
                    jsonObject['error'] = "None"
                    json.dump(jsonObject, make_file, ensure_ascii=False, indent="\t")
                break
            else:
                add_error(file_name)
        
        print_log('\n[End of Process]\n')
        
        
            
    except IndyError as e:
        add_error(file_name)
        print('Error occurred: %s' % e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_did())
    loop.close()


if __name__ == '__main__':
    main()



