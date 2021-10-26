import asyncio
from collections import OrderedDict
import time
import json
import pprint
import sys
import logging
from indy import pool, ledger, wallet, did
from indy.error import IndyError, ErrorCode
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION, add_error, print_log, POOL_NAME

admin_did = sys.argv[1]
user_did = sys.argv[2]

att_year = sys.argv[3]
att_month = sys.argv[4]

file_name = user_did + "_attrib.json"

pool_name = POOL_NAME
genesis_file_path = get_pool_genesis_txn_path(pool_name)

async def get_attrib_transaction():
    try:
        await pool.set_protocol_version(PROTOCOL_VERSION)

        print_log('genesis_txn: ', genesis_file_path)

        # 1.
        print_log('\n1. Open pool ledger and get handle from libindy\n')
        pool_handle = await pool.open_pool_ledger(config_name=pool_name, config=None)

        # 2.
        print_log('\n2. Get Attrib Transaction in Month & Make "attrib.json" File\n')
        count = 0

        # Export Attrib Tx to json
        with open(file_name,'w',encoding="utf-8") as make_file:
            data = {}
            data['error'] = "None"
            data['did'] = admin_did
            data['transaction'] = []
            
            # 월마다의 말일 설정
            last_day = 30
            if int(att_month) % 2 == 1 or int(att_month) == 8:
                last_day = 31

            for building in range(1, 10):                
                for i in range(1, last_day+1):
                    if i < 10:
                        raw = user_did + '_' + str(building) + '_' + att_year + att_month + "0" + str(i)
                    else:
                        raw = user_did + '_' + str(building) + '_' + att_year + att_month + str(i)
                    try:
                        get_attrib_request = await ledger.build_get_attrib_request(admin_did,admin_did,raw, None, None)
                        get_attrib_response = json.loads(await ledger.submit_request(pool_handle, get_attrib_request))

                        if get_attrib_response['result']['data'] is not None:
                            count = count + 1
                            
                            print_log("Success")
                            response = json.loads(get_attrib_response['result']['data'])
                            data["transaction"].append(response[raw])

                        else:
                            pass

                    except IndyError as ex:
                        if ex.error_code == ErrorCode.LedgerInvalidTransaction:
                            print_log(ex.error_code)
                            pass
                        else:
                            with open(file_name,'w',encoding="utf-8") as make_file:
                                json.dump(json.loads(response), make_file, ensure_ascii=False, indent="\t")
                                
            print_log("Count: " + str(count))
            if count == 0:
                data['error'] = "Error"
                json.dump(data, make_file, ensure_ascii=False,indent="\t")
            else:
                json.dump(data, make_file, ensure_ascii=False,indent="\t")

        print_log('\n[End of Process]\n')

    except IndyError as e:
        print('Error occurred: %s' %e)
        add_error(file_name)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_attrib_transaction())
    loop.close()


if __name__ == '__main__':
    main()

