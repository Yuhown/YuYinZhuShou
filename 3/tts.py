from aip import AipSpeech
import pygame
import json

class Robot():
    def __init__(self,per=1,speed=5,pit=5,vol=5,listen_time=5):
         # 设置语速，取值范围0-9，默认为5(中语速)
        self.speed = speed
        # 选择发音人，0为普通女声音（默认），1为普通男声，3为度逍遥等
        self.per = per
        # 选择音调，取值范围0-9，默认为5(中语调)
        self.pit = pit
         # 选择音量，取值范围0-15，默认为5(中音量)
        self.vol = vol
        self.machine_mp3 = 'audio/machine1.mp3'# 音频保存路径
        self.client = None  # 初始化登录信息为空
    def login(self):
        # 打开百度账号文本文件
        with open('./data/LoginInfo.txt', 'r') as fp:  
            info = json.loads(fp.read())  #登录信息转换成JSON数据
        #根据登录信息创建百度云语音接口，以实现语音识别和语音合成
        self.client = AipSpeech(info['appid'], info['apikey'], info['secretkey'])       
    """播放音频"""
    def play(self,file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
    def run(self):
        pygame.mixer.init()
        try:
            self.login()
            print("登录成功...")
        except:
            print("登录失败...")
            # 进行语音合成，正确则返回语音二进制，错误则返回dict
        result  =  self.client.synthesis(str("你好呀"), 'zh', 1,{'vol':self.vol,'spd':self.speed,'per':self.per,'pit':self.pit})
        if not isinstance(result, dict):  
            with open(self.machine_mp3, 'wb') as f:
                f.write(result)
        self.play(self.machine_mp3)
    
if __name__ == "__main__":
    Robot(per=4,speed=3,pit=0,vol=1,listen_time=4).run()