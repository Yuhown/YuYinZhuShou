from aip import AipSpeech
import json
import requests
import pyaudio
import wave
import numpy as np
import time
import webbrowser
import time
import pygame
import os
import urllib
import serial
from selenium import webdriver
import re
import DCmotor_test

ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=1);   #open named port at 9600,1s timeot

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
        self.work = not True
        self.stop = not True
        self.starttime = 0
        self.nowtime = 0
        self.test = True
        #self.text_input = ""
        
    """下载音乐"""
    def get_music_url(name):
        driver.get('https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w='+name)
        driver.implicitly_wait(10)
        data = driver.find_element_by_xpath('//div[@class="songlist__item"]//a').get_attribute('href')
        data = {'mid' : data}
        print("data",data)
        return data

    def get_music(data):
        req = requests.post('http://www.douqq.com/qqmusic/qqapi.php',data=data).content
        req = json.loads(req.decode('utf-8'))
        #req = json.loads(req.decode('unicode'))
        req = req.replace('\/','/')
        g = re.compile('"m4a":"(.*?)",')
        c = re.findall(g,req)
        c = c[0]
        return c

    def save_music(c,name):
        os.makedirs('/music/',exist_ok=True)
        file_name = "%s.mp3" %name
        #file_path = os.path.join("/home/pi/Desktop/qq_music", file_name)  # only stitch English song's name
        file_path = "/music/" + file_name
        #file_path = file_path.decode('unicode')
        print("file_path",file_path)
        try:
            #urllib.request.urlretrieve( c , '/home/pi/Desktop/qq_music/' + name + '.mp3')
            urllib.request.urlretrieve( c , file_path)
        except:
            print("can't save the music")
            traceback.print_exc()

    def DownloadMusic(self, name):
        try:
            data = get_music_url(name)
            c = get_music(data)
            save_music(c,name)
            return 1
        except:
            return 0
    
    """初始化pygame模块"""
    def pygame_init(self):
        pygame.mixer.init()
    """播放音频"""
    def play(self,file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
    """pygame是否正忙"""
    def get_busy(self):
        return pygame.mixer.music.get_busy()
    """以二进制格式打开文件"""
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    """播放WAV"""
    def play_wav(self,file):
        """参数：wav文件绝对路径"""
        """阻塞，直到播放完成"""
        CHUNK = 1024
        wf = wave.open(file, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    """图灵机器人"""
    def answer(self, text_input):
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
                        "city":"shenzhen",
                        "province":"guangdong"
                    }
                }
            },
            "userInfo":
            {
                "apiKey":"6fff619804884decb5dd732f331d1ab1",
                #"text": self.questen,
                "userId":"szsy"
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
        print("response_dic['results'][0]",response_dic['results'][0])
        print("response_dic['results'][0]['values']",response_dic['results'][0]['values'])
        return response_dic['results'][0]['values']
        

    """MP3文件转WAV文件"""
    def mp3_to_wav(self,mp3,wav):
        """参数：MP3文件绝对路径，WAV文件绝对路径"""
        """输出：WAV文件"""
        sound = AudioSegment.from_mp3(mp3)  #加载mp3文件
        sound.export(wav, format="wav")  #转换格式
    
    """有声音就录音"""
    def recodeing(self,t):
        """参数：录音阈值，正常1500"""
        """阻塞，直到录音完成"""
        CHUNK = 4096  #每次读取的音频流长度
        FORMAT = pyaudio.paInt16  #语音文件的格式
        CHANNELS = 1  #声道数，百度语音识别要求单声道
        RATE = 8000  #采样率， 8000 或者 16000， 推荐 16000 采用率
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
    def login(self):
        with open('./data/LoginInfo03.txt', 'r') as fp:  #打开
            info = json.loads(fp.read())  #登录信息转换成JSON数据
        #根据登录信息创建百度云语音接口，以实现语音识别和语音合成
        self.client = AipSpeech(info['appid'], info['apikey'], info['secretkey'])
    def listening(self):
        while self.listen:
            self.recodeing(1500)
            print("开始上传音频数据...")
            result_text = self.client.asr(self.get_file_content(self.man_wav), 'wav',8000, {'dev_pid': '1537',})
            print('语音识别结果：')
            print(result_text)
            if 'result' in result_text.keys():
                info = result_text["result"][0][:-1]
                if self.test:
                    print('唤醒音识别结果：'+info)
                if info in self.name:
                    self.listen = not True
                    self.work = True
                    self.stop = not True
                    break
            else:
                if self.test:
                    print('识别失败')
    def working(self):
        self.play_wav(self.start_wav)
        self.starttime = time.time()
        while self.work:
            CHUNK = 4096  #每次读取的音频流长度
            FORMAT = pyaudio.paInt16  #语音文件的格式
            CHANNELS = 1  #声道数，百度语音识别要求单声道
            RATE = 8000  #采样率， 8000 或者 16000， 推荐 16000 采用率
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
                if temp >1500:
                    wait = not True
                    break
                self.nowtime = time.time()
                if self.nowtime-self.starttime>self.listen_time:
                    self.listen = True
                    self.work = not True
                    self.stop = not True
                    self.play_wav(self.stop_wav)
                    break
            if self.work:
                large_count = np.sum( audio_data > LEVEL )
                while large_count>8:
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
                #录音结束
                print("开始上传音频数据...")
                result_text = self.client.asr(self.get_file_content(self.man_wav), 'wav',8000, {'dev_pid': '1537',})
                if 'result' in result_text.keys():
                    self.questen = result_text["result"][0][:-1]
                    if self.test:
                        print('语音输入识别结果：'+self.questen)
                    if self.questen in ['机电了','点了','机电','电缆','电了','现在几点了']:#对时间的处理，‘几点了’的识别结果很无奈
                        now_time = time.localtime()
                        tm_hour = now_time.tm_hour
                        if tm_hour >= 12:
                            tm_hour -= 12
                        tm_min = now_time.tm_min
                        tm_sec = now_time.tm_sec
                        turing_answer_text = str(tm_hour)+'点'+str(tm_min)+'分'+str(tm_sec)+'秒'
                    elif self.questen in ['今天几号','今天多少号']:#对日期的处理
                        now_time = time.localtime()
                        tm_mon = now_time.tm_mon
                        tm_mday = now_time.tm_mday
                        turing_answer_text = str(tm_mon)+'月'+str(tm_mday)+'号'
                    elif self.questen in ['今天星期几']:#对星期的处理
                        now_time = time.localtime()
                        tm_wday = now_time.tm_wday+1
                        if tm_wday <= 6:
                            turing_answer_text = '星期'+str(tm_wday)
                        else:
                            turing_answer_text = '星期日'
                    elif self.questen in ['前进','向前进','前进了','go','后退','向后退','左转','向左转','右转','向右转','转圈','转圈儿']: 
                        if self.questen in ['前进','向前进','前进了','go']:
                            turing_answer_text = '好的'
                            DCmotor_test.car_forward()
                            DCmotor_test.stop()
                        else:
                            DCmotor_test.stop()
                    elif self.questen in ['停止播放','停止','别唱了']:
                        turing_answer_text = '好的'
                    elif self.questen in self.name:
                        turing_answer_text = '嗯！这儿了'
                    elif '播放' in self.questen:#对唱歌的处理
                        try:
                            self.play('music/'+self.questen[2:]+'.mp3')
                            continue
                        except:
                            turing_answer_text = '咱还没有下载这首歌呢'
                    elif '下载' in self.questen:#对唱歌的处理
                        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        self.play_wav(self.start_wav)
                        down_ok_or_not = self.DownloadMusic(self.questen[2:])
                        if down_ok_or_not:
                            turing_answer_text = '好了'
                        else:
                            turing_answer_text = '不好意思，我没有权限'
                    elif self.questen in ['说话快一点']:#对语速的处理
                        if self.speed < 9:
                            self.speed += 1
                        turing_answer_text = '好的，快了'
                    elif self.questen in ['说话慢一点']:#对语速的处理
                        if self.speed > 0:
                            self.speed -= 1
                        turing_answer_text = '好的，慢了'
                    elif self.questen in ['语调高一点','调高一点','音调高一点']:#对语调的处理
                        if self.pit < 9:
                            self.pit += 1
                        turing_answer_text = '好的，高了'
                    elif self.questen in ['语调低一点','调低一点','音调低一点']:#对语调的处理
                        if self.pit > 0:
                            self.pit -= 1
                        turing_answer_text = '好的，低了'
                    elif self.questen in ['打开即可供房','打开即刻供房','打开即刻供方']:#加入对网页的处理
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get('http://www.geek-workshop.com/forum.php')
                        #webbrowser.open('http://www.geek-workshop.com/forum.php')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开电影天堂']:#加入对网页的处理
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get('http://www.dytt8.net/')
                        #webbrowser.open('http://www.dytt8.net/')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开博客','打开CSDN博客','CSDN博客']:#加入对网页的处理
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get('https://blog.csdn.net/Lingdongtianxia')
                        turing_answer_text = '好的'
                    elif '搜索' in self.questen:#加入对网页的处理
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get('https://www.baidu.com/baidu?ie=utf-8&wd='+self.questen[2:])
                        #webbrowser.open('https://www.baidu.com/baidu?ie=utf-8&wd='+self.questen[2:])
                        turing_answer_text = '好的'
                    elif self.questen in ['打开CSDN下载','CSDN下载']:#加入对网页的处理
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get('https://download.csdn.net/my')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开木可','打开中国大学慕课']:#加入对网页的处理
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get('https://www.icourse163.org/')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开我的课程','我要当学霸','我要做学霸','我要学习']:#加入对网页的处理
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get('https://www.icourse163.org/home.htm?userId=1019112339#/home/course')
                        turing_answer_text = '好的'
                    elif self.questen in ['打开截图','截图','打开截屏','截屏']:#加入对软件的处理
                        #os.system(r"start D:\快速截图\FSCapture_单文件.exe")
                        os.system("scrot /home/pi/Desktop/example.png")
                        turing_answer_text = '好的'
                    elif self.questen in ['打开微信','微信']:#加入对软件的处理
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get("https://wx.qq.com/")
                        turing_answer_text = '好的'
                    elif self.questen in ['打开邮箱','邮箱']:#加入对软件的处理
                        my_driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
                        my_driver.get("https://mail.qq.com")
                        turing_answer_text = '好的'

                    elif self.questen in ['左手','举左手']:#加入对软件的处理
                        ser.write(b"2")
                        turing_answer_text = '左手'

                    elif self.questen in ['右手','举右手']:#加入对软件的处理
                        ser.write(b"3")
                        turing_answer_text = '右手'
                    elif self.questen in ['摇头']:#加入对软件的处理
                        ser.write(b"4")
                        turing_answer_text = '头好晕啊'

                    elif self.questen in ['领导','领导好']:#加入对软件的处理
                        ser.write(b"1")
                        turing_answer_text = '欢迎欢迎，热烈欢迎'
                    else:
                        turing_answer = self.answer(self.questen)   # todo
                        print("turing_answer",turing_answer)
                        turing_answer_text = turing_answer['text']
                        print("turing_answer_text",turing_answer_text)
                        if 'url' in turing_answer.keys():
                            webbrowser.open(turing_answer['url'])
                        if 'list' in turing_answer.keys():
                            webbrowser.open(turing_answer['list'][0]['detailurl'])
                            webbrowser.open(turing_answer['list'][1]['detailurl'])
                    if self.test:
                        print('图灵机器人的回答：'+turing_answer_text)
                    result  = self.client.synthesis(str(turing_answer_text), 'zh', 1,{'vol':self.vol,'spd':self.speed,'per':self.per,'pit':self.pit})
                    if not isinstance(result, dict):  
                        with open(self.machine_mp3, 'wb') as f:
                            f.write(result)
                    #self.mp3_to_wav(self.machine_mp3, self.machine_wav)
                    self.play(self.machine_mp3)
                    while self.get_busy():
                        time.sleep(0.2)
                    pygame.mixer.music.load(self.machine_wav)#使用pygame加载一个别的音频，释放掉self.machine_mp3，不然权限出错
                    time.sleep(0.2)#防止扬声器对麦克风的干扰
                    self.starttime = time.time()
    def run(self):
        self.pygame_init()
        try:
            self.login()
            print("登录成功...")
        except:
            print("登录失败...")
        while True:
            self.listening()
            print("录音完毕...")
            self.working()

