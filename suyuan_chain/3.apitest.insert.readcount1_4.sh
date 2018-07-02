#!/bin/sh
curl -s https://testnet.ninechain.net/api/v2.1 -H 'content-type:application/json' -H "X-Api-Key: 7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00" -d '{
    "data": "{\"params\": {\"channel\": \"notaryinfotestchannel\", \"records\": [{\"key\": \"1130102150229180616010000000001\", \"value\": \"hahaha1\", \"meta\": {\"readcount\": 1}}, {\"key\": \"1130102150229180616010000000002\", \"value\": \"hahahaha2\", \"meta\": {\"readcount\": 1}}, {\"key\": \"1130102150229180616010000000003\", \"value\": \"hahaha3\", \"meta\": {\"readcount\": 1}}, {\"key\": \"1130102150229180616010000000004\", \"value\": \"hahahaha4\", \"meta\": {\"readcount\": 1}}]}, \"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"source-insert-batch\"}",
    "nonce": "R8n9eO3SVDTYbQrkZMw75vLisxBdNo6l",
    "alg": "md5",
    "sign": "42c5829bf516808f7f3ff936f67d3ee0"
}'