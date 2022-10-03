from aip import AipSpeech
import json
import pyaudio
import wave
import numpy as np
import time
import pygame

class Robot():
    def __init__(self,name=['小明'],per=1,speed=5,pit=5,vol=5,listen_time=5):
        self.name = name
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
        with open('./data/LoginInfo04.txt', 'r') as fp:  #打开
            info = json.loads(fp.read())  #登录信息转换成JSON数据
        #根据登录信息创建百度云语音接口，以实现语音识别和语音合成
        self.client = AipSpeech(info['appid'], info['apikey'], info['secretkey']) 
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
        
    def recording(self,t):
        """参数：录音阈值，正常1500"""
        """阻塞，直到录音完成"""
        CHUNK = 4096  #每次读取的音频流长度
        FORMAT = pyaudio.paInt16  #语音文件的格式
        CHANNELS = 1  #声道数，百度语音识别要求单声道
        RATE = 16000  #采样率， 8000 或者 16000， 推荐 16000 采用率
        wait = True  #录音等待
        LEVEL = 1000
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,\
                        frames_per_buffer=CHUNK)
        frames = []
        while wait:
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
            temp = np.max(audio_data)
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
        self.recording(5000)
        result_text = self.client.asr(self.get_file_content(self.man_wav), 'wav',16000, {'dev_pid': '1537',})
        if 'result' in result_text.keys():
            info = result_text["result"][0][:-1]
            if self.test:
                print('唤醒音识别结果：'+info)     
        else:
            if self.test:
                print('识别失败')
        return info
    
    def play(self,file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        
    def tts(self,text):
        pygame.mixer.init()
        result  =  self.client.synthesis(str(text), 'zh', 1,{'vol':self.vol,'spd':self.speed,'per':self.per,'pit':self.pit})
        if not isinstance(result, dict):  
            with open(self.machine_mp3, 'wb') as f:
                f.write(result)
        self.play(self.machine_mp3)
        while pygame.mixer.music.get_busy():
            time.sleep(0.2)
            
    def run(self):
        try:
            self.login()
            print("登录成功...")
        except:
            print("登录失败...")
        while True:
            print("正在录音...")
            result = self.listening()
            if self.name in result:
                self.tts('你好')
            elif "诗" in result:
                self.tts('窗前明月光')
                self.tts('疑似地上霜')
                self.tts('举头望明月')
                self.tts('低头思故乡')
            elif "停止" in result:
                break
            elif '搜索' in result:
                my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                my_driver.get('https://www.baidu.com/baidu?ie=utf-8&wd='+"")
            else:
                self.tts('我不知道怎么回答你')
if __name__ == "__main__":
    Robot(name='你好',per=4,speed=3,pit=0,vol=1,listen_time=4).run()