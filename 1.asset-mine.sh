#!/bin/sh
curl -s https://testnet.ninechain.net/api/v2.1 -H 'content-type:application/json' -H "X-Api-Key: 7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00" -d '{
    "data": "{\"params\": {\"channel\": \"assettestchannel\", \"uid\": \"20180623112615001\", \"arr\": [{\"user\": \"userA\", \"amount\": 101000000}, {\"user\": \"userB\", \"amount\": 1010000000}]}, \"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"asset-mine\"}",
    "nonce": "R8n9eO3SVDTYbQrkZMw75vLisxBdNo6l",
    "alg": "md5",
    "sign": "6fecfca3a166df94beda5c6bede1d4f0"
}'