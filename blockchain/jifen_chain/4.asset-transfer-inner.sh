#!/bin/sh
curl -s https://testnet.ninechain.net/api/v2.1 -H 'content-type:application/json' -H "X-Api-Key: 7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00" -d '{
    "data": "{\"params\": {\"channel\": \"assettestchannel\", \"type\": \"inner\", \"uid\": \"20180623164901001\", \"arr\": [{\"from\": \"userA\", \"to\": \"userB\", \"amount\": 500000000}]}, \"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"asset-transfer\"}",
    "nonce": "R8n9eO3SVDTYbQrkZMw75vLisxBdNo6l",
    "alg": "md5",
    "sign": "756d60c68b95579b7582daeb2a23ad4d"
}'