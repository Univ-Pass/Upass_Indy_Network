from mnemonic import Mnemonic
import hashlib

mnemo = Mnemonic("english")
words = mnemo.generate(strength=128)
hash = hashlib.sha256(words.encode('utf-8')).hexdigest()

# print(words)
# print(hash)

print('Your Mnemonic(Write it down on Cold Storage with DID) : '+ words)
print('When setting the DID, enter it as the seed : '+ hash[0:32])