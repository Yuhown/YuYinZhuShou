#呼吸灯
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)
p=GPIO.PWM(7,100)
p.start(2)
#p.stop()
while True:
    for i in range(0,100,5):
        p.ChangeDutyCycle(i)
        time.sleep(0.1)
    for i in range(100,0,-5):
        p.ChangeDutyCycle(i)
        time.sleep(0.1)

GPIO.cleanup()