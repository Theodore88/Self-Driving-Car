# File: Motor.py
# Description: This file is designed to control the motors on the car based off the turn value calculated in Main.py
# Author: Theodore Hoang
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
 
class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.EnaA= EnaA
        self.In1A = In1A 
        self.In2A = In2A
        self.EnaB= EnaB
        self.In1B = In1B
        self.In2B = In2B
        # assign GPIO pins as output pins
        GPIO.setup(self.EnaA,GPIO.OUT)
        GPIO.setup(self.In1A,GPIO.OUT)
        GPIO.setup(self.In2A,GPIO.OUT) 
        GPIO.setup(self.EnaB,GPIO.OUT)
        GPIO.setup(self.In1B,GPIO.OUT)
        GPIO.setup(self.In2B,GPIO.OUT)

        #PWM pins/enable pins are for speed
        self.pwmA = GPIO.PWM(self.EnaA, 100) # Initialize PWM pins with frequency 100Hz
        self.pwmB = GPIO.PWM(self.EnaB, 100)
        #start speed at 0
        self.pwmA.start(0)
        self.pwmB.start(0)
        self.mySpeed=0
 
    def move(self,speed=0.5,turn=0,time=0):
        speed *=100 # Scale speed, so can use in changeDutyCycle
        turn *=70 # Scale turn
        leftSpeed = speed-turn # Negative turn means turn left
        rightSpeed = speed+turn
        
        #Set max motor speed to 100 and -100, so we can use it in ChangeDutyCycle()
        if leftSpeed>100: 
            leftSpeed =100 
        elif leftSpeed<-100: 
            leftSpeed = -100 
        if rightSpeed>100: 
            rightSpeed =100
        elif rightSpeed<-100: 
            rightSpeed = -100
        self.pwmA.ChangeDutyCycle(abs(rightSpeed)) # sets how much time PWM wave is on in a cycle
        self.pwmB.ChangeDutyCycle(abs(leftSpeed))
        # use "abs" because can't give negative speed to change duty cycle
        # changing duty cycle controls rotational speed of motor(changes speed)

        #DIRECTION CHANGE HANDLED HERE
        if rightSpeed>0:
            GPIO.output(self.In1A,GPIO.HIGH) # left side forward
            GPIO.output(self.In2A,GPIO.LOW)
        else:
            GPIO.output(self.In1A,GPIO.LOW) # left side backwards
            GPIO.output(self.In2A,GPIO.HIGH)
        if leftSpeed>0:
            GPIO.output(self.In1B,GPIO.HIGH)
            GPIO.output(self.In2B,GPIO.LOW)
        else:
            GPIO.output(self.In1B,GPIO.LOW)
            GPIO.output(self.In2B,GPIO.HIGH)
        sleep(time)
 
    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0) # Set PWM signals to always be low
        self.pwmB.ChangeDutyCycle(0)
        self.mySpeed=0
        sleep(t) # sleep for t seconds, stops car for t seconds
 
def main(): # main function used in the testing control of motors
    motor.move(0.5,0,2) 
    motor.stop(2)
    motor.move(-0.5,0,2)
    motor.stop(2)
    motor.move(0,0.5,2)
    motor.stop(2)
    motor.move(0,-0.5,2)
    motor.stop(2)
 
if __name__ == '__main__':
    motor= Motor(2,3,4,17,22,27) # Create motor object with pin numbers 
    main()
