from aip import AipSpeech # 引入Speech SDK
import json
with open('./data/LoginInfo.txt', 'r') as fp:   # 打开百度账号文本文件
    info = json.loads(fp.read())  #登录信息转换成JSON数据
        #根据登录信息创建百度云语音接口，以实现语音识别和语音合成
client = AipSpeech(info['appid'], info['apikey'],info['secretkey']) 
# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
# 识别本地文件
result=client.asr(get_file_content('01.wav'), 'wav', 16000,
                  {'dev_pid': 1537,})
print(result['result'])