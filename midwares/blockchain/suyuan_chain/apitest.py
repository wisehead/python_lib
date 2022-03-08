# encoding:utf-8
#!/usr/bin/env python

import json
import traceback

#############################################　默认参数　###################################################
#Version 1.3 
#su yuan test chain, batch info ok, package info testing. readcount.

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
Channel = "notaryinfotestchannel"

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

def test_source_put_binary():
    """
    创建二进制记录接口测试
    """
    params = {
        "channel": Channel,
        "key": "test/my2.pic",     # TODO 设置　要创建的记录的key。　如果已经存在些二进制文件(数据)，创建会失败
    }

    upload_file_path = "jiagong1.jpg"  # TODO 设置　要创建的记录对应的文件(数据)

    origin_params = {"params": params, "jsonrpc": "2.0", "id": 0, "method": "source-put-binary"}
    signed_params = get_signed_json(origin_params, SecretKey)

    url = DEFAULT_BINARY_URL
    cmd = "curl -s {0} -H 'content-type:multipart/form-data' -H \"X-Api-Key: {1}\" -F json='{2}' -F upload='@{3}'"\
        .format(url, ApiKey, json.dumps(signed_params, indent=4), upload_file_path)

    write_cmd(cmd)

    need_request = False            # TODO 设置　need_request＝True 会使用python第三方库requests发起请求，并打印结果
    if not need_request:
        return

    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    from requests_toolbelt.multipart.encoder import MultipartEncoder

    multipart_data = MultipartEncoder(
        fields={
            'upload': ('any', open(upload_file_path, 'rb'), 'text/plain'),
            'json': json.dumps(signed_params),
        },
    )

    res = requests.post(url, data=multipart_data, headers={'Content-Type': multipart_data.content_type, 'X-Api-Key':ApiKey})
    s = res.content.decode()
    signed_result = checkout_signed_json(s, SecretKey)
    if not signed_result:
        print("inavlid result: ", s)
        return

    print("================= signed_result is:")
    print(json.dumps(signed_result, indent=4))

    result = json.loads(signed_result["data"])
    print("=================result is:")
    print(json.dumps(result, indent=4))


def test_source_get_binary():
    """
        检索二进制记录接口测试
    """
    params = {
        "channel": Channel,
        "key": "test/my2.pic"      # TODO 设置　要查询的二进制记录的key
    }

    origin_params = {"params": params, "jsonrpc": "2.0", "id": 0, "method": "source-get-binary"}
    signed_params = get_signed_json(origin_params, SecretKey)
    print_cmd(signed_params, print_cmd=True)        # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　

    need_request = False        # TODO 设置　need_request＝True 会使用python第三方库requests发起请求，并打印结果
    if not need_request:
        return

    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    url = DEFAULT_URL
    res = requests.post(url, json=signed_params, headers={'content-type': 'application/json', 'X-Api-Key': ApiKey}, verify=False)
    s = res.content.decode()
    print(s)


def test_source_insert_batch():
    """
        批量创建记录接口测试
    """
    params = {
        "channel": Channel,
        "records": [
            {
                "key": "113010215022918061602",      # TODO 设置　记录的key。　在一次创建提交中，不要存在相同的key，否则只有一条会被记录到历史交易中
                "value": "hahaha1",       # TODO 设置　记录的value
            },
            {
                "key": "113010215022918061601",
                "value": "{\"batchNumber\":\"第一批次\",\"batchOutput\":\"10000斤（每斤一个最小包装单位）\",\"tasteScore\":\"84\",\"biologicalOrganicFertilizer\":{\"address\":\"哈尔滨市香坊区印染街1号\",\"brand\":\"归农稻花香有机米专用\",\"licenseNumberOfGreenFoodProductionData\":\"LSSZ-01-1503080005（中国绿色食品协会）\",\"manufacturer\":\"哈尔滨绿洲之星生物科技有限公司\",\"packageNumber\":\"G16号\",\"productMarking\":{\"mainTechnicalIndicators\":\"有效活菌数>=0.2亿/g  N+P2O5+K2O>=15% 有机质>=20%\",\"scientificAddition\":\"腐植酸>=12% 氨基酸>=1% 1酵素酶>=0.5亿/g中微量元素>=18% 有益微生物蛋白酶及生长促进未知因子(UGF)\"},\"productionTechnology\":\"酵素生物技术、复合微生物肥\",\"registrationNumberOfTheMinistryOfAgriculture\":\"微生物肥（2016）准字（1896号\",\"standardOfExecution\":\"NY/T798-2015\",\"website\":\"www-hrblz.com\"},\"detectionReportOfEmbryoRateAndIntegrity\":{\"picture1\":\"suyuan1/9.liupeilv1.png\",\"picture2\":\"suyuan1/10.liupeilv2.png\",\"picture3\":\"suyuan1/11.liupeilv3.png\",\"picture4\":\"suyuan1/12.liupeilv4.png\"},\"inspectionReport\":{\"approver\":\"张瑞英\",\"auditor\":\"马永华\",\"dateOfApproval\":\"2017-07-25\",\"dateOfAudit\":\"2017-07-25\",\"dateOfTabulation\":\"2017-07-25\",\"dateToSample\":\"2017-07-06\",\"experimentalEnvironmentConditions\":\"符合实验条件\",\"inspectionBasis\":\"NY/T 419-2014\",\"inspectionCategory\":\"委托\",\"inspectionConclusion\":\"该样品按NY/T 419-2014标准检验合格\",\"inspectionProject\":\"见报告第2页\",\"inspectionUnit\":\"五常市饭包儿水稻种植专业合作社\",\"items\":[{\"inspectionProject\":\"色泽、气味\",\"measurementUnit\":\"——\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"无异常色泽和气味\",\"testMethod\":\"GB/T 5492-2008\",\"testResults\":\"正常\"},{\"inspectionProject\":\"不完善粒\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=3.0\",\"testMethod\":\"GB/T 5494-2008\",\"testResults\":\"0.1\"},{\"inspectionProject\":\"杂质总量\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.25\",\"testMethod\":\"GB/T 5494-2008\",\"testResults\":\"0.00\"},{\"inspectionProject\":\"杂质糠粉\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.15\",\"testMethod\":\"GB/T 5494-2008\",\"testResults\":\"0.00\"},{\"inspectionProject\":\"杂质矿物质\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.02\",\"testMethod\":\"GB/T 5494-2008\",\"testResults\":\"0.00\"},{\"inspectionProject\":\"杂质带壳稗粒\",\"measurementUnit\":\"粒/kg\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=3\",\"testMethod\":\"GB/T 5494-2008\",\"testResults\":\"0\"},{\"inspectionProject\":\"杂质稻谷粒\",\"measurementUnit\":\"粒/kg\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=4\",\"testMethod\":\"GB/T 5494-2008\",\"testResults\":\"0\"},{\"inspectionProject\":\"碎米总量\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=7.5\",\"testMethod\":\"GB/T 5503-2009\",\"testResults\":\"2.3\"},{\"inspectionProject\":\"碎米中小碎米含量\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.5\",\"testMethod\":\"GB/T 5503-2009\",\"testResults\":\"0.0\"},{\"inspectionProject\":\"黄粒米\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.5\",\"testMethod\":\"GB/T 5496-1985\",\"testResults\":\"0.0\"},{\"inspectionProject\":\"互混\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=5.0\",\"testMethod\":\"GB/T 5493-2008\",\"testResults\":\"0.0\"},{\"inspectionProject\":\"水分\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=15.5\",\"testMethod\":\"GB/T 5497-1985\",\"testResults\":\"15.0\"},{\"inspectionProject\":\"直链淀粉含量（干基）\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"13.0-20.0\",\"testMethod\":\"NY/T 83-1988\",\"testResults\":\"17.89\"},{\"inspectionProject\":\"垩白度\",\"measurementUnit\":\"%\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=5\",\"testMethod\":\"NY/T 83-1988\",\"testResults\":\"0.5\"},{\"inspectionProject\":\"无机砷\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.15\",\"testMethod\":\"GB 5009.11-2014\",\"testResults\":\"0.057\"},{\"inspectionProject\":\"总汞\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB 5009.17-2014\",\"testResults\":\"0.0062\"},{\"inspectionProject\":\"磷化物\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB 5009.36-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"乐果\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.20-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"敌敌畏\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.20-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"马拉硫磷\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.20-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"杀螟硫磷\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.20-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"三唑磷\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.00034\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 20770-2008\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"克百威\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.00653\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 20770-2008\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"甲胺磷\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.004\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.103-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"杀虫双\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.002\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.114-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"溴氯菊酯\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.00088\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.110-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"水胺硫磷\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 20770-2008\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"稻瘟灵\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.155-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"三环唑\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.155-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"三环唑\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 5009.115-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"丁草胺\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.01\",\"testMethod\":\"GB/T 20770-2008\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"铅\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.2\",\"testMethod\":\"GB/T 5009.12-2010\",\"testResults\":\"0.04\"},{\"inspectionProject\":\"镉\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.2\",\"testMethod\":\"GB/T 5009.15-2014\",\"testResults\":\"0.013\"},{\"inspectionProject\":\"吡虫啉\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.011\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.05\",\"testMethod\":\"GB/T 20770-2008\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"噻嗪酮\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.01\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.3\",\"testMethod\":\"GB/T 5009.184-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"毒死蜱\",\"measurementUnit\":\"mg/kg\",\"methodDetectionLimit\":\"<0.008\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=0.1\",\"testMethod\":\"GB/T 5009.145-2003\",\"testResults\":\"未检出\"},{\"inspectionProject\":\"黄曲霉毒素B1\",\"measurementUnit\":\"ug/kg\",\"methodDetectionLimit\":\"——\",\"singleConclusion\":\"合格\",\"standardRequirements\":\"<=5.0\",\"testMethod\":\"GB/T 5009.22-2003\",\"testResults\":\"<5.0\"}],\"mainInstrumentsUsed\":\"气相色谱仪液相色谱质谱联用仪\",\"modelSpecification\":\"————\",\"originalNumberOrDateOfProduction\":\"————\",\"picture1Cover\":\"suyuan1/2.jianyan1.png\",\"pictureBaseSoil\":\"suyuan1/3.jianyan2.png\",\"pictureIrrigatedWaterSource\":\"suyuan1/4.jianyan3.png\",\"productionUnit\":\"————\",\"remarks\":\"只对来样负责\",\"sampleGradeAndState\":\"正常籽粒\",\"sampleMaker\":\"韩剑东\",\"sampleName\":\"有机大米\",\"sampleNumber\":\"2017C3152\",\"sampleQuantity\":\"5kg\",\"samplingBase\":\"————\",\"samplingSite\":\"————\",\"tabulatingPerson\":\"盛慧\",\"trademark\":\"————\"},\"organicCertificationOfBase\":{\"certificateNumber\":\"227OP1600099\",\"certificationBasis\":{\"item1\":\"GB/T19630.1-2011有机产品：生产\",\"item2\":\"GB/T19630.3-2011有机产品：标识与销售\",\"item3\":\"GB/T19630.4-2011有机产品：管理体系\"},\"pictureName\":\"suyuan1/1.youji.png\"},\"patentInfo\":[{\"patentCertificateNumber\":\"第1978111号\",\"patentName\":\"稻谷碾白机\",\"pictureName\":\"suyuan1/5.zhuanli1.png\"},{\"patentCertificateNumber\":\"第2619488号\",\"patentName\":\"胚芽米精磨机\",\"pictureName\":\"suyuan1/6.zhuanli2.png\"},{\"patentCertificateNumber\":\"第6479912号\",\"patentName\":\"一种双室胚芽米碾米机\",\"pictureName\":\"suyuan1/7.zhuanli3.png\"},{\"patentCertificateNumber\":\"第6479920号\",\"patentName\":\"一种米糠、谷壳粉碎装置\",\"pictureName\":\"suyuan1/8.zhuanli4.png\"}],\"positionInformation\":{\"position1PlantingBaseLocation\":\"127.03833333333333E, 45.03777777777778N\",\"position2StorageBaseLocation\":\"127.06222222222222E, 45.05583333333333N\",\"position3ProcessingBaseLocation\":\"126.81805555555556E, 45.780277777777776N\"},\"productInspectionReport\":{\"picture1\":\"suyuan1/16.baogao1.png\",\"picture2\":\"suyuan1/17.baogao2.png\"},\"seedInfo\":{\"breedsOwner\":\"五常市利元种子有根公司\",\"cropSpecies\":\"稻\",\"dateOfDetection\":\"2017年11月 批号：0191\",\"firstBreeders\":\"田永太\",\"grade\":\"国家保护品种\",\"informationCode\":\"0125727100017593\",\"licenseNumberOfSeedProductionAndOperation\":\"C(黑哈五)农种许字(2016)第6001号\",\"netContent\":\"25kg\",\"numberOfPlantQuarantineCertificates\":\"2301842017001091\",\"qualityExecutionStandard\":{\"grainLength\":\"16.0%\",\"headRiceRate\":\"85%\",\"polishedRiceRate\":\"98.0%\",\"standardName\":\"GB4404.1-2008\",\"unpolishedRiceRate\":\"99.9%\"},\"qulity\":{\"gelConsistency\":\"67.0%\",\"grainLength\":\"6.6mm\",\"headRiceRate\":\"66.8%\",\"polishedRiceRate\":\"75.7%\",\"tasteScore\":\"88-92\",\"unpolishedRiceRate\":\"84.1%\"},\"registeredAddress\":\"黑龙江省五常市龙凤山镇乐园村汪家店屯\",\"seedCategory\":\"常规种原种\",\"seedProducer\":\"五常市利元种子有限公司\",\"varietyApprovalNumber\":\"黑审稻2009005 吉审稻2016011\",\"varietyName\":\"五优稻4号\",\"varietyRightsNumber\":\"CNA20080376.X\",\"website\":\"www.clxseed.com\"}}",
            }
        ]
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "source-insert-batch", print_cmd=True, need_request=False)


def test_source_transactions():
    """
        查询历史交易记录接口测试
    """
    params = {
        "channel": Channel,
        #"key": "mytest/1",      # TODO 设置　要查询的记录的key
        "key": "1130102150229180616010000000004",      # TODO 设置　要查询的记录的key
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "source-transactions", print_cmd=True, need_request=False)


def test_source_transaction():
    """
        检索交易记录接口测试
    """
    params = {
        "channel": Channel,
        "key": "00000000000000000000000000000111",  # TODO 设置　要查询的记录的key
        #"tx_id": "e84a8ce75c279fa42c05b0860dd25a5a0f5cf4e198f6a157f04b1c4332eda829"     # TODO 设置　要查询交易ID, 此ID由 source-insert-batch, source-put-binary生成，并且可以从source-transactions查询到
        "tx_id": "345bf63a8381a5486df16733cea2b1256bb6c8ad5400e7b87f616d0755c0d983"     # TODO 设置　要查询交易ID, 此ID由 source-insert-batch, source-put-binary生成，并且可以从source-transactions查询到
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "source-transaction", print_cmd=True, need_request=False)


def test_source_state():
    """
        检索最新状态接口测试
    """
    params = {
        "channel": Channel,
        #"key": "00000000000000000000000000000111",  # TODO 设置　要查询的记录的key
        #"key": "1130102150229180616010000000001",  # TODO 设置　要查询的记录的key
        "key": "1130102150229180616010000000005",  # TODO 设置　要查询的记录的key
        #"key": "113010215022918061601",  # TODO 设置　要查询的记录的key
        #"key": "mytest/6",  # TODO 设置　要查询的记录的key
    }

    # TODO 设置　print_cmd=True 会把curl命令写到./apitest.sh中　
    # TODO 设置　need_request=True 会使用python第三方库requests发起请求，并打印结果
    request_common(params, "source-state", print_cmd=True, need_request=False)


if __name__ == "__main__":
    #############################################　参数设置　###################################################
    ApiKey = "7a79d668d61993119516d7c898aa072bb971467752e3e7bb2751cc474080db00"             # TODO 设置　用户的ApiKey
    SecretKey = "3072c26dedb17d5545e53099fced54d30e13ad7f98a0ca542a73549535540600"       # TODO 设置　用户的密钥
    Channel = "notaryinfotestchannel"            # TODO 设置　用户的子链channel

    try:
        # TODO 选择要测试的接口，一次只能打开一个！！！

         test_source_insert_batch()
        #test_source_transactions()
        # test_source_transaction()
        #test_source_state()
        # test_source_put_binary()
        # test_source_get_binary()
    except Exception as e:
        traceback.print_exc()
        print(e)


# TODO 使用前必读　
# TODO 1. 使用python3执行此脚本　
# TODO 2. 在前面测试函数中，print_cmd=True 会把curl访问的命令写到./apitest.sh中，可以修改参数，执行此脚本，并使用./apitest.sh验证
# TODO 3. 在前面测试函数中，need_request=True 在此脚本发起请求，并打印结果。要使用此功能，请先使用python3的包管理工具，安装python3扩展库requests和requests_toolbelt # TODO 4. 此测试脚本包括了客户使用时的签名算法，可以参考　
