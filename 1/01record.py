import pyaudio#引入所用库文件
import wave

CHUNK = 1024#定义数据流块 
FORMAT = pyaudio.paInt16
#表示我们使用量化位数16位来进行录音
CHANNELS = 1 #代表的是声道，这里使用的单声道
RATE = 16000#采样率16k，每秒采样16000个点
RECORD_SECONDS = 5#录制时间这里设定了5秒
WAVE_OUTPUT_FILENAME = "01.wav"
p = pyaudio.PyAudio()#创建音频流
stream = p.open(format=FORMAT,#音频流wav格式
                channels=CHANNELS,#单声道
                rate=RATE,#采样率16000
                input=True,
                frames_per_buffer=CHUNK)

def record(stream):
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #计算要读多少次，每秒的采样率/每次读多少数据=需要读多少次
        data = stream.read(CHUNK)#每次读chunk个数据
        frames.append(data)#将读出的数据保存到列表中
    return frames

def save(frames):
    stream.stop_stream()#停止数据流
    stream.close()#关闭输入流
    p.terminate()#关闭 PyAudio
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#以'wb'二进制流写的方式打开一个文件
    wf.setnchannels(CHANNELS)#设置音轨数
    wf.setsampwidth(p.get_sample_size(FORMAT))
#设置采样点数据的格式，和FOMART保持一致
    wf.setframerate(RATE)#设置采样率与RATE要一致
    wf.writeframes(b''.join(frames))
#将声音数据写入文件
    wf.close()#关闭文件流，释放句柄

if __name__ == "__main__":
    print("开始录音,请说话......")
    frames  = record(stream)
    print("录音结束!")
    save(frames)

