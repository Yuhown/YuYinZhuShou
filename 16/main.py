from aip import AipSpeech
import json
import pyaudio
import wave
import numpy as np
import time
import pygame
import urllib
from util import DCmotor_control
from util import DCservo_control
from selenium import webdriver
from download import download
from play_music import play_music
from turing_answer import answer
from play import play
from recording import recording, check_env_voice
from move_old_version import move
class Robot():
    def __init__(self,name,per=1,speed=5,pit=5,vol=5,listen_time=5):
        self.name = name
        self.speed = speed
        self.per = per
        self.pit = pit
        self.vol = vol
        self.listen_time = listen_time
        self.man_wav = 'audio/man.wav'
        self.machine_mp3 = 'audio/machine.mp3'
        self.start_wav = 'audio/start.wav'
        #self.sleep_wav = 'audio/sleep.wav'
        self.stop_wav = 'audio/stop.wav'
        self.move = ['左手','右手','前','后','左转','右转','转圈','摇头']
        with open('./data/LoginInfo.txt', 'r') as fp:  #打开
            info = json.loads(fp.read())  #登录信息转换成JSON数据        
        self.client = AipSpeech(info['appid'], info['apikey'], info['secretkey']) #根据登录信息创建百度云语音接口，以实现语音识别和语音合成
        self.test = True
        DCservo_control.init()
        self.search_flag = 0
        self.download_flag = 0
        self.sleep = 0
        pygame.mixer.init()
    
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
        
    def tts(self,text):
        result  =  self.client.synthesis(str(text), 'zh', 1,{'vol':self.vol,'spd':self.speed,'per':self.per,'pit':self.pit})
        if not isinstance(result, dict):  
            with open(self.machine_mp3, 'wb') as f:
                f.write(result)
        play(self.machine_mp3)
        while pygame.mixer.music.get_busy():
            time.sleep(0.2)
            
    def listening(self):
        env_voice = check_env_voice()
        while True:
            recording(env_voice=env_voice)
            with open(self.man_wav, 'rb') as fp:
                file = fp.read()
            result_text = self.client.asr(file, 'wav',16000, {'dev_pid': '1537',})
            if 'result' in result_text.keys():
                info = result_text["result"][0][:-1]
                print('唤醒音识别结果：'+info)
                if self.sleep == 0:#判断是否已经唤醒
                    if self.name not in info:#如果语音识别结果不是唤醒词，则播放“请说唤醒词”
                        self.tts('请说唤醒词')
                        continue
                    else:
                        self.tts('你好啊')#如果语音识别为唤醒词，则更该状态为唤醒状态，并退出此次问答
                        self.sleep =1
                        continue
                if  self.search_flag == 1 or self.download_flag == 1:#判断是否为下载或者搜索模式，
                    if self.search_flag == 1:#如果是搜索模式则直接用网友搜索识别到的关键词
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get('https://www.baidu.com/baidu?ie=utf-8&wd='+info)
                        answer_text ='网页开好了'
                        self.search_flag = 0#完成搜索后，关闭搜索模式
                    else:
                        download(info)#如果是下载模式，则直接下载歌名
                        print("输入 pause暂停播放,play继续播放,stop停止播放")
                        play_music()
                        answer_text = "音乐放完了"
                        self.download_flag = 0
                elif info is None or info == '':
                    answer_text = "没听清，可以再说一遍吗？"
                else:
                    if info in ['机电了','点了','机电','电缆','电了','现在几点了']:#对时间的处理，‘几点了’的识别结果很无奈
                        now_time = time.localtime()
                        tm_hour = now_time.tm_hour
                        if tm_hour >= 12:
                            tm_hour -= 12
                        tm_min = now_time.tm_min
                        tm_sec = now_time.tm_sec
                        answer_text = str(tm_hour)+'点'+str(tm_min)+'分'+str(tm_sec)+'秒'
                    elif '今天几号' in info or '今天多少号' in info:#对日期的处理
                        now_time = time.localtime()
                        tm_mon = now_time.tm_mon
                        tm_mday = now_time.tm_mday
                        answer_text = str(tm_mon)+'月'+str(tm_mday)+'号'
                    elif '今天星期几' in info:#对星期的处理
                        now_time = time.localtime()
                        tm_wday = now_time.tm_wday+1
                        if tm_wday <= 6:
                            answer_text = '星期'+str(tm_wday)
                        else:
                            answer_text = '星期日'
                    elif "诗" in info:#如果不是下载或搜索模式，则进行关键词检测
                        self.tts('床前明月光')
                        self.tts('疑似地上霜')
                        self.tts('举头望明月')
                        self.tts('低头思故乡')
                        answer_text = "念完了"
                    elif "停止" in info:#如果是停止指令，则播放“再见”，并取消唤醒，并跳出本次循环
                        self.tts('再见')
                        self.sleep =0
                        continue
                    elif '搜索' in info:#进入到搜索模式
                        answer_text = "你要搜索什么"
                        self.search_flag = 1
                    elif '下载' in info:#进入到下载模式
                        answer_text = "你要听什么音乐"
                        self.download_flag = 1
                    else:#先判动作列表，如果没有动作则使用图灵机器人
                        move_order ={}#新建一个动作列表存放动作的顺序
                        for key in self.move:#判断语音中是否有指定的动作，动作列表在init中有定义
                            if info.find(key) != -1:#查找每一个的动作是否在识别结果中
                                i= 0
                                while i < len(info):#逐一判断每个动作在识别结果中的位置，从第0位开始到文本结束
                                    if info.find(key,i) == -1:#string.find（）函数如果没有找到动作则会返回－1，这里如果检测到－1则跳出检测
                                        break
                                    else:
                                        move_order[key+str(i)] = info.find(key,i)#由于dict字典类的key不能重复，故将动作名称后加上该动作在文本中的位置，防止key重复
                                        i = move_order[key+str(i)]+1
                            else :
                                result = None#如果没有检测到动作，则将结果显示为None
                        move_list= sorted(move_order.items(), key=lambda d:d[1], reverse = False)#根据动作列表的数值顺序，排列动作列表，列表是有顺序的，dict是没有顺序
                        for key in move_list:#遍历动作列表
                            result= move(key[0])#分别传入每个列表的key，
                            self.tts(result)
                        if result == None:
                            answer_text = answer(info)#如果没有识别到的动作则调用图灵机器人的问答接口
                        else:
                            continue
            else:
                answer_text = "没听清"#防止百度接口调用失败报错
                print('语音识别接口调用失败')
            self.tts(answer_text)#统一将回答语句播报出来
            
if __name__ == "__main__":
    Robot("你好",per=4,speed=3,pit=0,vol=1,listen_time=4).listening()
