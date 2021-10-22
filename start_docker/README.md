# Indy-API

```
cd start_docker
docker build -t client_docker .

docker images # 제대로 이미지가 만들어 졌는지 확인

sh ./client_start.sh "docker_image" "Github ID" "Github PW"

docker ps # 도커 컨테이너가 제대로 실행이 되었는지 확인

sh ./api.sh "CONTAINER_ID 또는 NAME" "이메일 해시값"   # 도커 컨테이너에 접근하여 원격으로 DID를 발급받고 해당 결과를 텍스트 파일로 리턴
```



# How to use

## sh_generate_did

```
Script for Generate DID
main source : generate_did.py
ex) sh sh_generate_did "container id" "wallet name" "wallet key" "student id(seed)"
```



## sh_change_pw

```
Script for Change Wallet Key
main source : recreate_wallet.py, indy-cli(with specific command txt file), set_metadata.py
ex) sh sh_generate_did "container id" "wallet name" "wallet key" "student id(seed)"
```

## sh_get_did

```
Script for get DID
main source : get_did.py
ex) sh sh_get_did "container id" "wallet name" "wallet key"
```

## sh_import_did

```
Script for import DID to new wallet
main source : import_did.py, indy-cli(with specific command txt file)
ex) sh sh_import_did "container id" "wallet name" "previous wallet key" "new wallet key" "student id(seed)"
```

## sh_regenerate_did

```
Script for import previous DID to new wallet
main source : export_did.py, indy-cli(with specific command txt file), set_metadata.py, export_wallet_id
ex) sh sh_regenerate_did "container id" "did" "student id(seed)" "email" "wallet name" "wallet key"
```

## sh_generate_attrib

```
Script for generate Attrib Tx
main source : generate_attrib.py
ex) sh sh_regenerate_did "container id" "wallet name" "wallet key" "admin_did" "user_did" "building number" "year" "month" "day"
```

## sh_get_attrib

```
Script for get Attrib Tx
main source : get_attrib.py
ex) sh sh_regenerate_did "container id" "admin_did" "user_did" "year" "month"
```

## update_docker
```
Script for Update Docker (in docker files)
in sh file: docker_list="docker container IDs" (Tokenize using withe space)
sh ./update_docker.sh
```
