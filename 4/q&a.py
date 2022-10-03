from aip import AipSpeech
import json
import pyaudio
import wave
import numpy as np
import time

class Robot():
    def __init__(self,name=['小明'],per=1,speed=5,pit=5,vol=5,listen_time=5):
        self.name = name
        self.speed = speed
        self.per = per
        self.pit = pit
        self.vol = vol
        self.listen_time = listen_time#从唤醒开始保持唤醒的时间
        self.man_wav = 'audio/man.wav'#人声录音的路径
        self.machine_mp3 = 'audio/machine.mp3'#机器回答文件路径
        self.machine_wav = 'audio/machine.wav'#仅用于pygame的临时加载
        self.start_wav = 'audio/start.wav'#开始的声音文件路径
        self.stop_wav = 'audio/stop.wav'#结束的声音文件路径
        self.client = None
        self.test = True
    
    def login(self):
        with open('./data/LoginInfo.txt', 'r') as fp:  
            info = json.loads(fp.read()) 
        self.client = AipSpeech(info['appid'], info['apikey'], info['secretkey']) 
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    def recording(self,t):
        CHUNK = 4096  #每次读取的音频流长度
        FORMAT = pyaudio.paInt16  #语音文件的格式
        CHANNELS = 1  #百度语音识别要求单声道
        RATE = 16000  #采样率
        wait = True  #录音等待
        LEVEL = 1500 #声音保存的音量阈值
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        print("开始录音")#提示文字出现后可开始录音
        #持续录音，当音量大于阈值t时，才执行接下来的程序
        while wait:
            data = stream.read(CHUNK) # 读取数据
            audio_data = np.fromstring(data, dtype=np.short) # 转为矩阵
            temp = np.max(audio_data)# 取矩阵中的最大值
            print(temp)#显示音量实时数值，方便检测调试
            if temp >t:
                wait = not True
         # 计算大于音量阈值的取样个数
        large_count = np.sum( audio_data > LEVEL )
        # 如果个数大于10，则将数据保存到frames列表中
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
        self.recording(5000)# 设置录音阈值为5000
         # 识别语音，转为文字
        result_text = self.client.asr(self.get_file_content(self.man_wav), 'wav',16000, {'dev_pid': '1537',})
        #print('语音识别结果：')
        if 'result' in result_text.keys():
            info = result_text["result"][0][:-1]
            # 如果完成识别，显示识别结果
            if self.test:
                print('唤醒音识别结果：'+info)
            # 如果识别结果里有关键字，则打印机器的回答
            if self.name in info:
                print("你好帅哥，你好美女")
            else:
                print("没有唤醒词")
        else:
            if self.test:
                print('识别失败')
                
if __name__ == "__main__":
    Robot(name='你好',per=4,speed=3,pit=0,vol=1,listen_time=4).listening()