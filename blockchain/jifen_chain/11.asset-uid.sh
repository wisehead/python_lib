#!/bin/sh
curl -s https://testnet.ninechain.net/api/v2.1 -H 'content-type:application/json' -H "X-Api-Key: 7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00" -d '{
    "data": "{\"params\": {\"channel\": \"assettestchannel\", \"uid\": \"20180623142625001\", \"type\": \"all\", \"arr\": [\"userA\", \"userB\"]}, \"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"asset-uid\"}",
    "nonce": "R8n9eO3SVDTYbQrkZMw75vLisxBdNo6l",
    "alg": "md5",
    "sign": "fec2083a791cd166c3b9917cf5104681"
}'