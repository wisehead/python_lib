# encoding:utf-8
#!/usr/bin/env python

import json
import traceback

#############################################　默认参数　###################################################
#Version JF 1.0
#Version 1.3 
#jifen initial version.

# NBCAPID_URL_21="http://localhost:8989/api/v2.1"
#NBCAPID_URL_21="https://www.ninechain.net/api/v2.1"  # 服务器url地址
NBCAPID_URL_21="https://testnet.ninechain.net/api/v2.1"  # 服务器url地址
# NBCAPID_BINARY_URL_21 = "http://localhost:8989/api/file/v2.1"
#NBCAPID_BINARY_URL_21 = "https://www.ninechain.net/api/file/v2.1"
NBCAPID_BINARY_URL_21 = "https://testnet.ninechain.net/api/file/v2.1"

DEFAULT_URL = NBCAPID_URL_21
DEFAULT_BINARY_URL = NBCAPID_BINARY_URL_21

ApiKey = "7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00"
SecretKey = "3072c26dedb17d5545e53099fced54d30e13ad7f98a0ca542a73549535540600"
TxId = ""
#Channel = "notaryinfotestchannel"
Channel = "assettestchannel"

#############################################　公共函数　###################################################

def calc_sign(**kwargs):
    # 组织成[key, value]数组的样式
    arr = [[k, v] for k, v in kwargs.items() if v]
    arr.sort()

    # 把排序后的value，拼接成一个字符串
    data_arr = [r[1] for r in arr]
    s = "".join(data_arr)
    print("string is:", s)

    # 计算md5签名
    import hashlib
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()


def get_random_string():
    import random
    import string

    # 生成随机字符串
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))

def get_signed_json(params, secret_key):
    """
    使用secret_key对参数params进行签名，返回签名后的请求
    """

    # 生成随机字符串
#chenhui
    #nonce = get_random_string()
    nonce = "R8n9eO3SVDTYbQrkZMw75vLisxBdNo6l" 

    # 编码原始参数成一个字符串
    data = json.dumps(params)

    # 可选参数：签名算法使用md5
    alg = "md5"

    # 示例不使用timestamp和deadline这两个可选参数。要使用时，去掉相关注释就可以了
    # timestamp = str(int(time.time()))
    # deadline = str(int(time.time()) + 5)

    # 用私钥签名
    sign = calc_sign(data=data, alg=alg, nonce=nonce, secret_key=secret_key, x=None)
    print("sign is:" , sign)

    # 返回带签名的请求
    signed_data = {
        "data": data,
        "nonce": nonce,
        "alg": alg,
        # "timestamp":  timestamp,
        # "deadline": deadline,
        "sign":sign
    }

    return signed_data


def checkout_signed_json(s, secret_key):
    """
    对返回结果进行签名验证，并返回结果
    """

    # 服务器端在签名验证完成前，如果出错，会返回　{"error":xxx}
    res = json.loads(s)
    error = res.get("error")
    if error:
        print("error result: ", s)
        return None

    signed_json = res

    # data和nonce是必选字段，如果不存在，signed_json["data"]直接抛异常
    data = signed_json["data"]
    nonce = signed_json["nonce"]

    # alg, deadline, timestamp是可选字段, 如果不存在，　signed_json.get("alg")返回None，不抛异常
    alg = signed_json.get("alg")
    deadline = signed_json.get("deadline")
    timestamp = signed_json.get("timestamp")

    sign = calc_sign(data=data, nonce=nonce, alg=alg, deadline=deadline, timestamp=timestamp, secret_key=secret_key)

    if sign == signed_json["sign"]:
        return signed_json

    return None


def write_cmd(cmd):
    filename = "./apitest.sh"
    with open(filename, "wb") as fp:
        fp.write("#!/bin/sh\n".encode())
        fp.write(cmd.encode())
    print("chmod +x {0}; sh -c {0}".format(filename))


def print_cmd(jsondata, print_cmd=True, **kwargs):
    """
    把curl命令写到文件，并提示用法
    """
    if not print_cmd:
        return

    url = DEFAULT_URL
    cmd = "curl -s {0} -H 'content-type:application/json' -H \"X-Api-Key: {1}\" -d '{2}'".format(url, ApiKey, json.dumps(jsondata, indent=4))
    write_cmd(cmd)


def do_request(signed_params, need_request=False, **kwargs):
    """
    使用python第三方库requests发起请求，并输出结果
    """
    if not need_request:
        return

    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url = DEFAULT_URL

    # 在头部带上ApiKey, 数据类型为'application/json'
    res = requests.post(url, json=signed_params, headers={'content-type': 'application/json', 'X-Api-Key':ApiKey}, verify=False)
    s = res.content.decode()
    signed_result = checkout_signed_json(s, SecretKey)
    if not signed_result:   # 失败
        print("inavlid result: ", s)
        return

    # 打印带签名的结果
    print("================= signed_result is:")
    print(json.dumps(signed_result, indent=4))

    # 打印不带签名的结果　
    result = json.loads(signed_result["data"])
    print("=================result is:")
    print(json.dumps(result, indent=4))


def request_common(params, method, **kwargs):
    """
    使用jsonrpc2组织请求
    """
    origin_params = {"params": params, "jsonrpc": "2.0", "id": 0, "method": method}
    signed_params = get_signed_json(origin_params, SecretKey)
    print_cmd(signed_params, **kwargs)
    do_request(signed_params, **kwargs)


#############################################　测试函数　###################################################
#1.用户挖矿
def test_asset_mine():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        #"uid": "20180623112615000001",
        #"uid": "20180623142625001",
        "uid": "20180623153325001",
        "arr": [
            {
                "user": "userA",      # TODO 设置　记录的key。　在一次创建提交中，不要存在相同的key，否则只有一条会被记录到历史交易中
                "amount": 10100000000000,       # TODO 设置　记录的value
            },
            {
                "user": "userB",      # TODO 设置　记录的key。　在一次创建提交中，不要存在相同的key，否则只有一条会被记录到历史交易中
                "amount": 101000000000,       # TODO 设置　记录的value
            }
        ]
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-mine", print_cmd=True, need_request=False)


#2.用户资源回收
def test_asset_transfer_recycle():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "type": "recycle",
        "uid": "20180623152729001",
        "arr": [{"user": "userA"}]
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-transfer", print_cmd=True, need_request=False)

#3.用户购买商品
def test_asset_transfer_buy():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "type": "buy",
        "uid": "20180623162021001",
        "arr": [{"user": "userA", "amount": 200000000}]
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-transfer", print_cmd=True, need_request=False)

#4.用户间转账
def test_asset_transfer_inner():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "type": "inner",
        "uid": "20180623164901001",
        "arr": [{"from": "userA", "to": "userB", "amount": 500000000}]
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-transfer", print_cmd=True, need_request=False)

#5.小柿饼兑换摩根币
def test_asset_exchange_xsb2mgb():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "type": "xsb2mgb",
        "uid": "20180623165901001",
        "arr": [{"user": "userA", "amount": 500000000}]
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-exchange", print_cmd=True, need_request=False)

#6.摩根币兑换小柿饼
def test_asset_exchange_mgb2xsb():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "type": "mgb2xsb",
        "uid": "20180623171001001",
        "arr": [{"user": "userA", "amount": 100000000}]
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-exchange", print_cmd=True, need_request=False)

#7.官方小柿饼兑换摩根币
def test_asset_exchange():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "type": "exchange",
        "uid": "20180623172301001",
        "amount": 100000000
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-exchange", print_cmd=True, need_request=False)

#8.查询用户积分
def test_asset_state():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "arr": ["userA", "userB"]
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-state", print_cmd=True, need_request=False)

#9.查询用户历史纪录
def test_asset_history():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "user": "userA",
        "start": 0,
        "count": 5000 
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-history", print_cmd=True, need_request=False)

#10.uid检索状态
def test_asset_uid_status():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "uid": "20180623142625001"
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-uid-status", print_cmd=True, need_request=False)

#12.uid检索结果
def test_asset_uid():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        #"uid": "20180623142625001",
        "uid": "20180623172301001",
        "type": "all",
        "arr": ["userA", "userB"]
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "asset-uid", print_cmd=True, need_request=False)

if __name__ == "__main__":
    #############################################　参数设置　###################################################
    ApiKey = "7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00"             # TODO 设置　用户的ApiKey
    SecretKey = "3072c26dedb17d5545e53099fced54d30e13ad7f98a0ca542a73549535540600"       # TODO 设置　用户的密钥
    #Channel = "notaryinfotestchannel"            # TODO 设置　用户的子链channel
    Channel = "assettestchannel"            # TODO 设置　用户的子链channel

    try:
        # TODO 选择要测试的接口，一次只能打开一个！！！

        #test_asset_mine()
        #test_asset_transfer_recycle()
        #test_asset_transfer_buy()
        #test_asset_transfer_inner()
        #test_asset_exchange_xsb2mgb()
        #test_asset_exchange_mgb2xsb()
        #test_asset_exchange()
        #test_asset_state()
        #test_asset_history()
        #test_asset_uid_status()
        test_asset_uid()
    except Exception as e:
        traceback.print_exc()
        print(e)


# TODO 使用前必读　
# TODO 1. 使用python3执行此脚本　
# TODO 2. 在前面测试函数中，print_cmd=True 会把curl访问的命令写到./apitest.sh中，可以修改参数，执行此脚本，并使用./apitest.sh验证
# TODO 3. 在前面测试函数中，need_request=True 在此脚本发起请求，并打印结果。要使用此功能，请先使用python3的包管理工具，安装python3扩展库requests和requests_toolbelt # TODO 4. 此测试脚本包括了客户使用时的签名算法，可以参考　
