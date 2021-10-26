import asyncio
from collections import OrderedDict
import json
import pprint
import sys
import datetime

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
admin_did = sys.argv[3]

# DID of visitant
user_did = sys.argv[4]

att_building = sys.argv[5]
att_year = sys.argv[6]
att_month = sys.argv[7]
att_day = sys.argv[8]

att_date = att_year+"-"+att_month+"-"+att_day
file_name = wallet_name + "_gen_attrib.json"

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
        did_result = await did.get_my_did_with_meta(wallet_handle, admin_did)
        # print_log('DID_Result ', did_result)
        
        # 4.
        print_log('\n4. Generate Attrib Transaction\n')

        time = datetime.datetime.now().time()
        dateformat = "%H:%M"
        time = time.strftime(dateformat)
        
        # Save Transactions log
        attrib_transaction_request = await ledger.build_attrib_request(admin_did, admin_did,None, 
        '{"'+user_did + '_' + att_building + '_' + att_year + att_month + att_day + '":{"time": "' + time +
         '", "name":"' + user_did + '", "building":"' + att_building
         + '", "date": "' + att_date + '"}}', None)

        attrib_transaction_response = await ledger.sign_and_submit_request(pool_handle=pool_handle,
                                                                        wallet_handle=wallet_handle,
                                                                        submitter_did=admin_did,
                                                                        request_json=attrib_transaction_request)
        print_log(attrib_transaction_response)

        # Set value of json
        json_data = {}
        json_data['error'] = "None"
        json_data['entry_date'] = att_date
        json_data['building_num'] = att_building
        json_data['entry_did'] = user_did
        json_data['entry_time'] = time

        # Export json of Tx info
        with open(file_name,'w',encoding="utf-8") as make_file:
            json.dump(json_data, make_file, ensure_ascii=False,indent="\t")

        print_log('\n[End of Process]\n')

    except IndyError as e:
        add_error(file_name)
        print('Error occurred: %s' %e)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_attrib_transaction())
    loop.close()


if __name__ == '__main__':
    main()

