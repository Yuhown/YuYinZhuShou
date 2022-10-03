import json
import urllib
import requests

def answer(text_input):
    """参数：中文问题；返回：JSON格式回答信息"http://www.tuling123.com/openapi/api",new:http://openapi.tuling123.com/openapi/api/v2"""
    api_url = "http://openapi.tuling123.com/openapi/api/v2"
    req = {
        "perception":# 信息参数
        {
            "inputText": # 文本信息
            {
                "text":text_input
                },
            "selfInfo":# 用户参数
            {
                "location":
                {
                    "city":"shanghai",# 所在城市
                    "province":"shanghai",# 省份
                    "street":"kangjianlu"# 街道
                }
            }
        },
        "userInfo":
        {
            "apiKey":"6fffdd71ab1",# 改为自己申请的key
            "userId":"Yi"# 用户唯一标识(随便填, 非密钥)
        }
    }
    #将字典对象转化为JSON对象，再编码为uft-8
    req = json.dumps(req).encode('utf8')
    #构造一个请求头，其中定义了传输格式
    http_post = urllib.request.Request(api_url,data=req,
                                       headers={'content-type':'application/json'})
    #打开url网址，参数可以是一个url，也可以是一个request对象
    response = urllib.request.urlopen(http_post)
    #获得网页源码的字符串str
    response_str = response.read().decode('utf8')
    #将str类型的数据转换为dict类型
    response_dic = json.loads(response_str)
    #将解析的结果保存为对象属性
    intent_code = response_dic['intent']['code']
    results_text = response_dic['results'][0]['values']['text']
    return response_dic['results'][0]['values']
    
if __name__ == "__main__":
    resuit = answer('你最近怎么样？')
    resuit = resuit['text']
    print(resuit)