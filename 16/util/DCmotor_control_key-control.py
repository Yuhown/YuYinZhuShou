#!/usr/bin/python
from Raspi_MotorHAT.Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
import pygame
import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
myMotor1 = mh.getMotor(1)
myMotor2 = mh.getMotor(2)
myMotor3 = mh.getMotor(3)

# M1 set the speed to start, from 0 (off) to 255 (max speed)
#myMotor1.setSpeed(50)
# M2
#myMotor2.setSpeed(50)
# M3
#myMotor3.setSpeed(50)

def car_forward():
    myMotor2.setSpeed(50)
    myMotor3.setSpeed(50)
    myMotor2.run(Raspi_MotorHAT.FORWARD)
    myMotor3.run(Raspi_MotorHAT.FORWARD)
    time.sleep(2.0)

def car_backward():
    myMotor2.setSpeed(50)
    myMotor3.setSpeed(50)
    myMotor2.run(Raspi_MotorHAT.BACKWARD)
    myMotor3.run(Raspi_MotorHAT.BACKWARD)
    time.sleep(2.0)
	
def car_left():
    myMotor1.setSpeed(50)
    myMotor2.setSpeed(50)
    myMotor3.setSpeed(50)
    myMotor1.run(Raspi_MotorHAT.FORWARD)
    myMotor2.run(Raspi_MotorHAT.FORWARD)
    myMotor3.run(Raspi_MotorHAT.RELEASE)
    time.sleep(2.0)
	
def car_right():
    myMotor1.setSpeed(50)
    myMotor2.setSpeed(50)
    myMotor3.setSpeed(50)
    myMotor1.run(Raspi_MotorHAT.BACKWARD)
    myMotor2.run(Raspi_MotorHAT.BACKWARD)
    myMotor3.run(Raspi_MotorHAT.RELEASE)
    time.sleep(2.0)
def around_right():
    myMotor1.setSpeed(50)
    myMotor2.setSpeed(50)
    myMotor3.setSpeed(50)
    myMotor1.run(Raspi_MotorHAT.FORWARD)
    myMotor2.run(Raspi_MotorHAT.BACKWARD)
    myMotor3.run(Raspi_MotorHAT.FORWARD)
    time.sleep(2.0)
def stop():
    myMotor1.run(Raspi_MotorHAT.RELEASE)
    myMotor2.run(Raspi_MotorHAT.RELEASE)
    myMotor3.run(Raspi_MotorHAT.RELEASE)
    time.sleep(0.1)

# key control car
def main():
    pygame.init()
    pygame.display.set_mode((1,1))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_input = pygame.key.get_pressed()
                print("w,a,d:",key_input[pygame.K_w],key_input[pygame.K_a],key_input[pygame.K_d])
                if key_input[pygame.K_w] and not key_input[pygame.K_a] and not key_input[pygame.K_d]:
                    car_forward()         # forward
                    #stop()
                elif key_input[pygame.K_a]:
                    car_left()            # left
                    #stop()
                elif key_input[pygame.K_d]:
                    car_right()           # right
                    #stop()
                elif key_input[pygame.K_s]:
                    car_backward()        # backward
                elif key_input[pygame.K_e]:
                    around_right()        # around right
                    
            elif event.type == pygame.KEYUP:
                stop()
                    


if __name__=="__main__":
    #car_forward()
    #car_backward()
    #car_left()
    #car_right()
    #around_right()  # around
    #stop()
    main()   # key control




