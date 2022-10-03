#!/usr/bin/python
#from Emakefun_MotorHAT.Emakefun_MotorHAT import Emakefun_MotorHAT, Raspi_DCMotor
from .Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_Servo
import time
import atexit

# create a default object, no changes to I2C address or frequency
#mh = Emakefun_MotorHAT(addr=0x6f)
mh = Emakefun_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
#	mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
#	mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)
#	mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)

	

atexit.register(turnOffMotors)

################################# DC motor test!
myMotor1 = mh.getMotor(1)
myMotor2 = mh.getMotor(2)

# M1 set the speed to start, from 0 (off) to 255 (max speed)
#myMotor1.setSpeed(35)
# M2
#myMotor2.setSpeed(35)
# M3
#myMotor3.setSpeed(35)

def car_forward():
    myMotor1.setSpeed(35)
    myMotor2.setSpeed(35)
    myMotor2.run(Emakefun_MotorHAT.FORWARD)
    myMotor1.run(Emakefun_MotorHAT.BACKWARD)
    time.sleep(1)
    
    myMotor1.run(Emakefun_MotorHAT.RELEASE)
    myMotor2.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.1)

def car_backward():
    myMotor1.setSpeed(40)
    myMotor2.setSpeed(35)
    myMotor2.run(Emakefun_MotorHAT.BACKWARD)
    myMotor1.run(Emakefun_MotorHAT.FORWARD)
    time.sleep(1)
    
    myMotor1.run(Emakefun_MotorHAT.RELEASE)
    myMotor2.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.1)
	
def car_left():
    myMotor1.setSpeed(30)
    myMotor2.setSpeed(30)
    myMotor1.run(Emakefun_MotorHAT.BACKWARD)
    myMotor2.run(Emakefun_MotorHAT.BACKWARD)
    time.sleep(0.3)
    
    myMotor1.run(Emakefun_MotorHAT.RELEASE)
    myMotor2.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.1)
	
def car_right():
    myMotor1.setSpeed(30)
    myMotor2.setSpeed(30)
    myMotor1.run(Emakefun_MotorHAT.FORWARD)
    myMotor2.run(Emakefun_MotorHAT.FORWARD)
    time.sleep(0.3)
    
    myMotor1.run(Emakefun_MotorHAT.RELEASE)
    myMotor2.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.1)
    
def around_right():
    myMotor1.setSpeed(35)
    myMotor2.setSpeed(35)
    myMotor1.run(Emakefun_MotorHAT.BACKWARD)
    myMotor2.run(Emakefun_MotorHAT.BACKWARD)
    time.sleep(2.0)
    
def stop():
    myMotor1.run(Emakefun_MotorHAT.RELEASE)
    myMotor2.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(0.1)

if __name__=="__main__":
    #car_forward()
    #car_backward()
    #car_left()
    #car_right()
    around_right()  # around
    stop()




