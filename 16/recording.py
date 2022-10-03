from play import play
import pyaudio
import numpy as np
import wave
import time
def recording():
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
        while wait:
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
            temp = np.max(audio_data)
            print("当前音量:"+str(temp))
            if temp >5000 and temp <30000:
                wait = not True
        large_count = np.sum( audio_data > LEVEL )
        while large_count>100:
            print('large_count', large_count)
            frames.append(data) 
            data = stream.read(CHUNK)
            audio_data = np.fromstring(data, dtype=np.short)
            large_count = np.sum( audio_data > LEVEL )
            print('large_count2', large_count)
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
    recording()