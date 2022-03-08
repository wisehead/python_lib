#!/bin/sh
curl -s https://testnet.ninechain.net/api/v2.1 -H 'content-type:application/json' -H "X-Api-Key: 7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00" -d '{
    "data": "{\"params\": {\"channel\": \"assettestchannel\", \"type\": \"recycle\", \"uid\": \"20180623152729001\", \"arr\": [{\"user\": \"userA\"}]}, \"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"asset-transfer\"}",
    "nonce": "R8n9eO3SVDTYbQrkZMw75vLisxBdNo6l",
    "alg": "md5",
    "sign": "e261f9dacdcdaede17eaa5da3636621e"
}'