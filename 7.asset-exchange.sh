#!/bin/sh
curl -s https://testnet.ninechain.net/api/v2.1 -H 'content-type:application/json' -H "X-Api-Key: 7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00" -d '{
    "data": "{\"params\": {\"channel\": \"assettestchannel\", \"type\": \"exchange\", \"uid\": \"20180623172301001\", \"amount\": 100000000}, \"jsonrpc\": \"2.0\", \"id\": 0, \"method\": \"asset-exchange\"}",
    "nonce": "R8n9eO3SVDTYbQrkZMw75vLisxBdNo6l",
    "alg": "md5",
    "sign": "c9010ebe358931466ee1bfa9e2b6f8ed"
}'