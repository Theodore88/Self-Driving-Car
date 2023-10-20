# File: Main.py
# Description: This file is designed to be initialized by the Raspberry Pi and control the operation of the car based on the curve value
# returned from LaneDetection.py
# Author: Theodore Hoang
from Motor import Motor
from LaneDetection import getLaneCurve
import Webcam
import cv2

# Specifying GPIO pin numbres
motor = Motor(2,3,4,17,22,27) # EnaA = 2, In1A = 3, In2A = 4, EnaB= 17, In1B = 22, In2B = 27
 
def main():
 
    img = Webcam.getImg() # Get image from webcam 
    curveVal= getLaneCurve(img,1) 
 
    sen = 1  # sen, how much more of impact we want to have on a curve
    maxVAl= 0.3 # maxVal, speed range from 0 to 1(max curve Val allowed)

    # Set curveVal equal to max values in the case of large curve values calculated
    if curveVal>maxVAl:
        curveVal = maxVAl
    if curveVal<-maxVAl: 
        curveVal =-maxVAl
    if curveVal>0:
        if curveVal<0.05: 
            curveVal=0  # Go straight if curveVal is super small
    else:
        if curveVal>-0.08: 
            curveVal=0 # Keep thresholds for negative and postive different cause of defects/differences in motor
    
    motor.move(0.20,curveVal*sen,0.05) # speed = 0.2, turn = curveVal*sen, time = 0.05
    cv2.waitKey(1)
     
 
if __name__ == '__main__':
    while True:
        main()