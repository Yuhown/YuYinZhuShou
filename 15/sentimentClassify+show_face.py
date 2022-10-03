from aip import AipNlp
import json
import time
import cv2

class Robot():
    def __init__(self,name=['小明'],per=1,speed=5,pit=5,vol=5,listen_time=5):
        self.name = name
        self.speed = speed
        self.per = per
        self.pit = pit
        self.vol = vol
        self.listen_time = listen_time
        self.client = None
    
    def login(self,text):
        with open('./data/LoginInfo05.txt', 'r') as fp:  #打开
            info = json.loads(fp.read())  #登录信息转换成JSON数据
        #根据登录信息创建百度云语音接口，以实现语音识别和语音合成
        self.client = AipNlp(info['appid'], info['apikey'], info['secretkey'])
        result = self.client.sentimentClassify(text)
        #print(result)
        confidence = result["items"][0]["confidence"]
        if confidence > 0.8:
            result = result["items"][0]["negative_prob"]
            if result < 0.5:
                print("正面情感")
                pic = cv2.imread("./720/smile.jpg")
                cv2.namedWindow("vision",1) #1 代表窗口大小等于图片大小,不可以被拖动改变大小.   
                cv2.imshow("vision",pic)
                cv2.moveWindow("vision",0,100)
                cv2.waitKey(0)
            else:
                print("负面情感") 
                pic = cv2.imread("./720/cry.jpg")
                cv2.namedWindow("vision",1) #1 代表窗口大小等于图片大小,不可以被拖动改变大小.   
                cv2.imshow("vision",pic)
                cv2.moveWindow("vision",0,100)
                cv2.waitKey(0)    
        else:
            print("未知的情感态度")
        time.sleep(1)#等待1秒钟，避免超过帐号qts
if __name__ == "__main__":
    Robot(name='你好',per=4,speed=3,pit=0,vol=1,listen_time=4).login("开心")