#输出控制（闪烁的灯）

#导入GPIO模块
import RPi.GPIO as GPIO 
#导入时间模块
import time

#设置编码模式
GPIO.setmode(GPIO.BCM)
#设置GPIO针脚的状态
GPIO.setup(7, GPIO.OUT)

#控制灯的亮灭
while True:
    GPIO.output(7, 1)
    time.sleep(2)
    GPIO.output(7, GPIO.LOW)
    time.sleep(2)
#脚本结束后进行清理
GPIO.cleanup()