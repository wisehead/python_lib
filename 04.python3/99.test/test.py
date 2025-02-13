import requests
import json

APP_ID = 398
QUESTIONS=["2024年公司销售合同额牵引目标是多少？目前完成情况如何，完成了目标的百分之多少？","截止到2024年11月，公司累计完成销售合同额是多少？11月当月完成销售合同额是多少？","请用柱状图给出各部门2024年1-9月，牵引目标完成情况","请给出2024年6月到9月之间，连续3个月牵引目标未完成的部门","请用三折线图给出2022-2024年近三年累计销售合同额的对比情况","请用柱状图给出2022-2024年近三年公司各业务类型累计销售合同额对比情况","请用柱状图给出2022-2024年近三年公司各细分战略累计销售合 同额对比情况","请给出云事业部2024年9月当月项目销售合同额，以及2024年1-9月累计项目销售合同额完成情况","请给出内部运维2024年9月当月，以及2024年1-9月累计销售合同额完成情况","请给出2024年1-9月累计合同签约额分布前三名的内部客户，分别占比是 多少","2024年公司外部业务牵引目标完成情况怎么样，同比如何？","2024年公司内部项目分类分为几类，其中自研类项目1-9月累计销售合同额是多少？","2024年公司外部业务客户金额前3名的是哪些，分别是什么类型的项目？","公司2024年9月销售预测是多少"," 请用柱状图给出各部门2024年10月销售预测与实际执行的对比情况","请问公司24年累计未转化商机还有多少","公司销售合同包括哪几个类别？","2024年公司销售合同额牵引目标是多少？目前完成情况如何，完成了目标的百分之多少？","截止到2024年11月，公司累 计完成销售合同额是多少？11月当月完成销售合同额是多少？","请用柱状图给出各部门2024年1-9月，牵引目标完成情况"]
KB_IDS = []
LLM_NAME = "Qwen2.5-72B-32K-B" # "ernie-4.0-8k", "Qwen2.5-72B-32K-B", "QWen2.5-72B-Instruct","jiutian_75b"

def lizhen_conversation_benchmark(app_id):
    print("============== 2")
    token = "5A568225331CBAD9881A1C3921BF78A725D89627DA45FA9F879F4908F394F4EC8D3794A9A1AF45C5B024DAE2108B233B"
    questions=QUESTIONS
    questions=questions*(200//len(questions))
    questions = questions[:100]

    question_id=1

    #RETRIEVE_URL=f"http://localhost:8000/chains/apps/conversations/stream"
    #RETRIEVE_URL=f"http://10.146.70.240:8000/chains/apps/conversations/stream"
    RETRIEVE_URL=f"http://ai.sinochem.com/ekc/stream-chat/chat/stream"
    #RETRIEVE_URL=f"http://ai.sinochem.com/ekc/chains/apps/conversations/stream"
    try:
        response = requests.post(RETRIEVE_URL,
                                data=json.dumps({
                                    "query": "hi", "appId": app_id, "externalUserId": "xxx@xxx.com", "history": [], "appType":0
                                    }
                                    ),
                            headers={
                                'accept': 'application/json',
                                'Content-Type': 'application/json',
                                "ekc-api-key": "a9af42064c514e88bca0bf40f64b13f0"
                            },
                            stream=True)

    except Exception as e:
        print(e)
        #return
    print(response)
    print("============== 3")
    # 打印响应内容（以文本形式）
    print("响应内容（文本形式）:")
    print(response.text)

    result=[]
    return response.text

# def main(query):
#     url = ""
#     headers = {}
#     data = {"query": "hi", "appId": 530, "externalUserId": "xxx@xxx.com", "history": [], "appType":0 }
#     result = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=10)
#     return {
#         "result": result.content
#     }

def main(intent) -> dict:
    print("============== 1")
    result = lizhen_conversation_benchmark(app_id=APP_ID)
    return {
        "intent": intent,
        "result": result
    }

if __name__ == "__main__":
    main("xxx")