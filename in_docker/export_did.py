import asyncio
from collections import OrderedDict
import json
import pprint
import sys
import re
from utils import get_pool_genesis_txn_path, PROTOCOL_VERSION, add_error, print_log, POOL_NAME

# Exported DID
did_db = sys.argv[1]

# User DID's Seed
student_seed = sys.argv[2]

file_name = student_seed + 'Did.json'

async def export_did():
    # Create DID File.
    print('\nParse DID \n')
    did_seed = "0000000000000000STUDENT" + student_seed
    result = {}
    result['version'] = 1
    result['dids'] = []
    _did = {}
    _did['did'] = did_db
    _did['seed'] = did_seed
    # _did['metadata'] = "StudentID"
    result['dids'].append(_did)

    ('\nExport DID \n')

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
