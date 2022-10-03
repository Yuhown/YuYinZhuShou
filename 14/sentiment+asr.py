from aip import AipSpeech
from aip import AipNlp
import json
import pyaudio
import wave
import numpy as np
import time
import pygame
import urllib



class Robot():
    def __init__(self,name=['小明'],per=1,speed=5,pit=5,vol=5,listen_time=5):
        self.speed = speed
        self.per = per
        self.pit = pit
        self.vol = vol
        self.listen_time = listen_time
        self.man_wav = 'audio/man.wav'
        self.machine_mp3 = 'audio/machine.mp3'
        self.machine_wav = 'audio/machine.wav'#仅用于pygame的临时加载
        self.start_wav = 'audio/start.wav'
        self.sleep_wav = 'audio/sleep.wav'
        self.stop_wav = 'audio/stop.wav'
        self.questen = ''
        self.client = None
        self.listen = True
        self.work = True
        self.stop = not True
        self.starttime = 0
        self.nowtime = 0
        self.test = True
        #self.text_input = ""
    
    def login(self):
        with open('./data/LoginInfo.txt', 'r') as fp:  #打开
            info = json.loads(fp.read())  #登录信息转换成JSON数据
        #根据登录信息创建百度云语音接口，以实现语音识别和语音合成
        self.client = AipSpeech(info['appid'], info['apikey'], info['secretkey']) 
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
        
        
    def recodeing(self,t):
        pygame.mixer.init()
        #pygame.mixer.music.load(self.machine_wav)#使用pygame加载一个别的音频，释放掉self.machine_mp3，不然权限出错
        #time.sleep(0.2)#防止扬声器对麦克风的干扰
        """参数：录音阈值，正常1500"""
        """阻塞，直到录音完成"""
        CHUNK = 4096  #每次读取的音频流长度
        FORMAT = pyaudio.paInt16  #语音文件的格式
        CHANNELS = 1  #声道数，百度语音识别要求单声道
        RATE = 16000  #采样率， 8000 或者 16000， 推荐 16000 采用率
        wait = True  #录音等待
        LEVEL = 1500
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,\
                        frames_per_buffer=CHUNK)
        frames = []
        print('开始录音')
        while wait:
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
            temp = np.max(audio_data)
            print(temp)
            if temp >t:
                wait = not True
        large_count = np.sum( audio_data > LEVEL )
        while large_count>10:
            frames.append(data) 
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
            large_count = np.sum( audio_data > LEVEL )
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(self.man_wav, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print('录音完毕...')
        
    def listening(self):
        self.login()
        self.recodeing(5000)
        print("开始上传音频数据...")
        result_text = self.client.asr(self.get_file_content(self.man_wav), 'wav',16000, {'dev_pid': '1537',})
        print('语音识别结果：')
        #print(result_text)
        if 'result' in result_text.keys():
            info = result_text["result"][0][:-1]
            if self.test:
                print('唤醒音识别结果：'+info)
            return info
                
        else:
            if self.test:
                print('识别失败')
                
    def sentiment(self):
        text = self.listening()
        with open('./data/LoginInfo05.txt', 'r') as fp:  
            info = json.loads(fp.read())  
        self.client = AipNlp(info['appid'], info['apikey'], info['secretkey'])
        result = self.client.sentimentClassify(text)#调用情感倾向分析，返回具体数值
        print(result)
        confidence = result["items"][0]["confidence"]
        if confidence > 0.8:
            result = result["items"][0]["negative_prob"]
            if result < 0.5:
                print("正面情感")
            else:
                print("负面情感")     
        else:
            print("未知的情感态度")
        time.sleep(1)#等待1s，避免超过帐号qps（Queries Per Second,每秒查询率）
                
if __name__ == "__main__":
    Robot(name=['你好'],per=4,speed=3,pit=0,vol=1,listen_time=4).sentiment()