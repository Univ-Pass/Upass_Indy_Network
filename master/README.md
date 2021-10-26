## Generate info_hash Attrib TX python for Master DID

```
Python code for Generate info_hash Attrib TX of Master DID
main source : master_post_info_hash.py
ex) python3 master_post_info_hash.py "wallet name" "wallet key" "master did" "student id" "학과" "경기대 지메일 ID(akqjqwk9@kyonggi.ac.kr(X) --> akqjqwk9(O) 도메인은 코드에서 알아서 추가해줌)"
```

- testpool은 코드를 바로 실행 가능
- mainpool은 실수를 방지하고자 입력창에 y를 넣어야 실행 됨

## Generate Mnemonic Words
```
Python code for Hashed generate Mnemonic Words(for Master DID's Seed)
main source : generate_seed.py
ex) python3 generate_seed.py
```

## Import Master DID
```
Script for Import Master DID to new wallet
main source : sh_import_master_did.py
ex) sh sh_import_master_did.sh "Master DID" "new wallet name" "new wallet key"
```

## Example Image of Cold Storage

<img src="./Example_ColdStorage.jpg">