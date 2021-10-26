import asyncio
from collections import OrderedDict
import json
import pprint
import sys
import re

# Exported DID
email = sys.argv[1]

# User DID's Seed
wallet_name = sys.argv[2]

# User Student ID
student_id = sys.argv[3]

file_name = student_id + 'NewWalletID.json'

async def export_wallet_id():
    # Make Json File to docker
    user_data = OrderedDict()
    user_data["email"] = email
    user_data["new_wallet"] = wallet_name
            
    # Generate new Wallet
    print('\nMake User EMail, New Wallet ID Json File\n')
    print(json.dumps(user_data, ensure_ascii=False, indent="\t"))

    # Export New Wallet ID
    with open(file_name,'w',encoding="utf-8") as make_file:
        user_data['error'] = "None"
        json.dump(user_data, make_file, ensure_ascii=False, indent="\t")

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(export_wallet_id())
    loop.close()


if __name__ == '__main__':
    main()
