#!/bin/sh
curl -s https://testnet.ninechain.net/api/v2.1 -H 'content-type:application/json' -H "X-Api-Key: 7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00" -d '{
    "data": "{\"params\": {\"channel\": \"assettestchannel\", \"user\": \"userA\", \"start\": 0, \"count\": 5000}, \"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"asset-history\"}",
    "nonce": "R8n9eO3SVDTYbQrkZMw75vLisxBdNo6l",
    "alg": "md5",
    "sign": "f29dbd59b04af0cde1265716adc44cd7"
}'