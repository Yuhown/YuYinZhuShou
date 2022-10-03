import json
import urllib
import requests

def answer(text_input):
    """参数：中文问题；返回：JSON格式回答信息"http://www.tuling123.com/openapi/api",new:http://openapi.tuling123.com/openapi/api/v2"""
    api_url = "http://openapi.tuling123.com/openapi/api/v2"
    req = {
        #"reqType":0,
        "perception":
        {
            "inputText":
            {
                "text":text_input
            },
            "selfInfo":
            {
                "location":
                {
                    "city":"shanghai",
                    "province":"shanghai",
                    "street":"kangjianlu"
                }
            }
        },
        "userInfo":
        {
            "apiKey":"4e02fe4a015545009f2cde225cdd3b2b",
            #"text": self.questen,
            "userId":"dengyuhong"
        }
    }
    #print("gyg01",req)
    req = json.dumps(req).encode('utf8')
    #print("gyg02",req)
    http_post = urllib.request.Request(api_url,data=req,headers={'content-type':'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    #print("response_str",response_str)
    response_dic = json.loads(response_str)
    #print("response_dic",response_dic)
    intent_code = response_dic['intent']['code']
    results_text = response_dic['results'][0]['values']['text']
    #print("response_dic['results']",response_dic['results'])
    #print("response_dic['results'][0]",response_dic['results'][0])
    #print("response_dic['results'][0]['values']",response_dic['results'][0]['values'])
    print(response_dic['results'][0]['values']['text'])
    return response_dic['results'][0]['values']['text']

if __name__ == "__main__":
    answer = answer('你好')
    print(answer)