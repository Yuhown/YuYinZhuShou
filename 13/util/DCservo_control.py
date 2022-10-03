#!/usr/bin/python

##from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM

from .Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_Servo
import time


# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
#pwm = PWM(0x6F)

mh = Emakefun_MotorHAT(addr=0x60)
"""
def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print ("%d us per period" % pulseLength)
  pulseLength /= 4096                     # 12 bits of resolution
  print ("%d us per bit" % pulseLength)
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 15, pulse)
"""
#myServo.writeServoFreq(50)                        # Set frequency to 60 Hz

myServol = mh.getServo(6)
myServor = mh.getServo(7)
myServoh = mh.getServo(8)

def init():
    myServol.writeServo(90)
    myServor.writeServo(10)
    myServoh.writeServo(95)
    
def raise_left_hand():      # raise left hand
    myServol.writeServo(90)
    time.sleep(2)
    myServol.writeServo(10)
    time.sleep(2)
    myServol.writeServo(90)
    time.sleep(2)
    
def raise_right_hand():     # raise right hand
    myServor.writeServo(10)
    time.sleep(2)
    myServor.writeServo(90)
    time.sleep(2)
    myServor.writeServo(10)
    time.sleep(2)
    
def shake_head():           # shake head
##    myServoh.writeServo(10)
##    time.sleep(2)
##    myServoh.writeServo(180)
##    time.sleep(2)
##    myServoh.writeServo(95)
##    time.sleep(2)
        
        myServoh.writeServo(95)
        for i in range (95, 125, 1):
            myServoh.writeServo(i)
            time.sleep(0.002)
        time.sleep(0.1)
        
        for a in range (0, 2, 1):
            for i in range (125, 65, -1):
                myServoh.writeServo(i)
                time.sleep(0.002)
            time.sleep(0.1)
            for i in range (65, 125, 1):
                myServoh.writeServo(i)
                time.sleep(0.002)
            time.sleep(0.1)
        
        for i in range (125, 95, -1):
            myServoh.writeServo(i)
            time.sleep(0.002)
        time.sleep(0.1)



if __name__=="__main__":
##    raise_left_hand()
##    print("ggggg")
##    raise_right_hand()
##    print("yyyyyy")
    shake_head()
    print("llllll")


