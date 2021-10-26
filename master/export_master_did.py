import asyncio
from collections import OrderedDict
import json
import pprint
import sys
import re
import hashlib
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION, add_error, print_log, POOL_NAME

# Exported DID
did_db = sys.argv[1]

# User DID's Seed
master_seed = sys.argv[2]

file_name = did_db + 'Did.json'

async def export_did():
    
    #mnemonic = input("Enter mnemonic : ")
    #hash_mnemonic = hashlib.sha256(mnemonic.encode('utf-8')).hexdigest()
    #master_seed = hash_mnemonic[0:32]

    # Create DID File.
    print_log('\n1. Parse DID \n')

    did_seed = master_seed
    result = {}
    result['version'] = 1
    result['dids'] = []
    _did = {}
    _did['did'] = did_db
    _did['seed'] = did_seed
    result['dids'].append(_did)

    print_log('\n2. Export DID \n')

    # Export DID file
    with open(file_name,'w',encoding="utf-8") as make_file:
        json.dump(result, make_file, ensure_ascii=False, indent="\t")
        print_log('\nExport DID Success!!\n')


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(export_did())
    loop.close()


if __name__ == '__main__':
    main()
