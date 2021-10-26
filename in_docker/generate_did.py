import asyncio
from collections import OrderedDict
import json
import pprint
import sys
from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION, add_error, print_log, POOL_NAME

pool_name = POOL_NAME
genesis_file_path = get_pool_genesis_txn_path(pool_name)

user_data = OrderedDict()

# User E-Mail Address
wallet_name = sys.argv[1]
wallet_key = sys.argv[2]
file_name = wallet_name + "_gen_did.json"
# User DID's Seed
student_seed = sys.argv[3]

wallet_config = json.dumps({"id": wallet_name})
wallet_credentials = json.dumps({"key": wallet_key})


async def create_did_and_write_nym():
    try:
        await pool.set_protocol_version(PROTOCOL_VERSION)

        print_log('genesis_txn: ', genesis_file_path)

        # 1.
        print_log('\n1. Open pool ledger and get handle from libindy\n')
        pool_handle = await pool.open_pool_ledger(config_name=pool_name, config=None)
       
        # 2.
        print_log('\n2. Creating new secure wallet\n')
        try:
            await wallet.create_wallet(wallet_config, wallet_credentials)
        except IndyError as ex:
            add_error(file_name)
            if ex.error_code == ErrorCode.WalletAlreadyExistsError:
                pass

        # 3.
        print_log('\n3. Open wallet and get handle from libindy\n')
        wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)

        # 4.
        print_log('\n4. Generating and storing steward DID and verkey\n')
        steward_seed = '000000000000000000000000Steward1'
        did_json = json.dumps({'seed': steward_seed})
        steward_did, steward_verkey = await did.create_and_store_my_did(wallet_handle, did_json)
        print_log('Steward DID: ', steward_did)
        print_log('Steward Verkey: ', steward_verkey)
        # Set DID's metadata
        await did.set_did_metadata(wallet_handle, steward_did, "Steward")

        # 5.
        print_log('\n5. Generating and storing trust anchor DID and verkey\n')
        did_seed = "0000000000000000STUDENT" + student_seed
        did_seed_json = json.dumps({'seed':did_seed})
        trust_anchor_did, trust_anchor_verkey = await did.create_and_store_my_did(wallet_handle, did_seed_json)
        print_log('Trust anchor DID: ', trust_anchor_did)
        print_log('Trust anchor Verkey: ', trust_anchor_verkey)
        await did.set_did_metadata(wallet_handle, trust_anchor_did, "StudentID")

        # 6.
        print_log('\n6. Building NYM request to add Trust Anchor to the ledger\n')
        nym_transaction_request = await ledger.build_nym_request(submitter_did=steward_did,
                                                                 target_did=trust_anchor_did,
                                                                 ver_key=trust_anchor_verkey,
                                                                 alias=None,
                                                                 role='TRUST_ANCHOR')
        print_log('NYM transaction request: ')
        pprint.pprint(json.loads(nym_transaction_request))

        # 7.
        print_log('\n7. Sending NYM request to the ledger\n')
        nym_transaction_response = await ledger.sign_and_submit_request(pool_handle=pool_handle,
                                                                        wallet_handle=wallet_handle,
                                                                        submitter_did=steward_did,
                                                                        request_json=nym_transaction_request)
        print_log('NYM transaction response: ')
        pprint.pprint(json.loads(nym_transaction_response))

        # Make Json File to docker
        user_data["email"] = wallet_name
        user_data["did"] = trust_anchor_did
        
        print_log('\n8. Make User EMail, DID Json File\n')
        print(json.dumps(user_data, ensure_ascii=False, indent="\t"))

        with open(file_name,'w',encoding="utf-8") as make_file:
            user_data['error'] = "None"
            json.dump(user_data, make_file, ensure_ascii=False, indent="\t")
        
        
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