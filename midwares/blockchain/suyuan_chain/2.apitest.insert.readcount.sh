#!/bin/sh
curl -s https://testnet.ninechain.net/api/v2.1 -H 'content-type:application/json' -H "X-Api-Key: 7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00" -d '{
    "data": "{\"params\": {\"channel\": \"notaryinfotestchannel\", \"records\": [{\"key\": \"1130102150229180616010000000005\", \"value\": \"hahaha3\", \"meta\": {\"readcount\": 1}}, {\"key\": \"1130102150229180616010000000006\", \"value\": \"hahahaha4\", \"meta\": {\"readcount\": 1}}]}, \"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"source-insert-batch\"}",
    "nonce": "R8n9eO3SVDTYbQrkZMw75vLisxBdNo6l",
    "alg": "md5",
    "sign": "805c099dd5456a80efe28b9551bdf2b5"
}'