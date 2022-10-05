from play import play
import pyaudio
import numpy as np
import wave
import time

def check_env_voice():
    print("环境音测试即将开始, 请保持安静.")
    time.sleep(1)
    CHUNK = 4096  #每次读取的音频流长度
    FORMAT = pyaudio.paInt16  #语音文件的格式
    CHANNELS = 1  #声道数，百度语音识别要求单声道
    RATE = 16000  #采样率， 8000 或者 16000， 推荐 16000 采用率
    wait = True  #录音等待
    LEVEL = 1500
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,\
                    frames_per_buffer=CHUNK)
    
    voice_sum = 0
    max_cnt = 20
    cnt = max_cnt
    while(cnt > 0):
        data = stream.read(CHUNK)
        audio_data = np.fromstring(data, dtype=np.short)
        # temp = np.sum( audio_data > LEVEL )
        temp = np.max(audio_data)
        print(temp, audio_data)
        voice_sum = voice_sum + temp
        cnt = cnt - 1
        
    avg_voice = voice_sum / max_cnt
    print("环境音测试已完成, 当前音量：", avg_voice)

    p.terminate()

    return avg_voice


def recording(env_voice=1500):
        """参数：录音阈值，正常1500"""
        """阻塞，直到录音完成"""
        """t为录音开始响度设置"""
        play('audio/start.wav')
        time.sleep(1)
        print("开始录音")
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
        voice = 0
        wait_cnt = 0            
        
        while wait:
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
          
            temp = np.max(audio_data)
            print("当前音量:"+str(temp))
            if temp > env_voice * 0.8:
                wait = not True
            else:
                voice = temp
            
        # large_count = np.max( audio_data > LEVEL )
        large_count = np.max(audio_data)
        while large_count > env_voice * 0.8:
            print('large_count=', large_count)
            frames.append(data) 
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
            large_count = np.max(audio_data)
            print('large_count2=', large_count)
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open('audio/man.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        play('audio/stop.wav')
        print('录音完毕...')
        
if __name__ == "__main__":
    print(check_env_voice())