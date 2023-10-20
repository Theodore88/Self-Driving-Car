# File: ColorDetection.py
# Description: This file is designed to capture and process video frames, allowing users to adjust the HSV color range 
# using trackbars and identify the correct HSV values to use in detecting a lane based on color.
# Author: Theodore Hoang

import cv2
import numpy as np 

#Initialize video capture
frameWidth = 640 # Specifying pixels
frameHeight = 480

cap = cv2.VideoCapture('demo.mp4') # Create videoCapture object using demo.mp4 in directory

def empty(): # Empty function that is called when trackbar created with cv2.createTrackbar is changed
    pass

# creating window for trackbar
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("Hue Min","HSV", 0, 179, empty) # Default value is 0 and max is 179, function 'empty is called everytime trackbar is changed
cv2.createTrackbar("Hue Max","HSV", 179, 179, empty) # Default value is 179 and max is 179
cv2.createTrackbar("Sat Min","HSV", 0, 255, empty)
cv2.createTrackbar("Sat Max","HSV", 255, 255, empty)
cv2.createTrackbar("Value Min","HSV", 0, 255, empty)
cv2.createTrackbar("Value Max","HSV", 255, 255, empty)

frameCounter = 0
while True:
    frameCounter += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter: # When video has reached the end loop back to beginning 
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter = 0
    success, img = cap.read() # Read frame from video and return whether frame was read succesfully and the frame itself
    
    
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Convert img from BGR color space to HSV color space

    hueMin = cv2.getTrackbarPos("Hue Min","HSV") # Return value from window named "HSV"
    hueMax = cv2.getTrackbarPos("Hue Max", "HSV")
    satMin = cv2.getTrackbarPos("Sat Min","HSV") 
    satMax = cv2.getTrackbarPos("Sat Max", "HSV")
    valueMin = cv2.getTrackbarPos("Value Min","HSV") 
    valueMax = cv2.getTrackbarPos("Value Max", "HSV")

    # Define lower and upper bounds of HSV color space that are to be extracted
    lower = np.array([hueMin,satMin,valueMin])
    upper = np.array([hueMax,satMax,valueMax])
        
    # Take frame in HSV colour space, any pixels that fall out of specified HSV bounds are black(0) in mask, pixels within bounds are white(1) in mask
    mask = cv2.inRange(imgHsv,lower,upper) 
    
    # Bitwise AND operation between mask and imgHsv is performed. If a pixel is white(1) in the mask and the pixel in the original image 
    # falls into the range specified by the mask it appears in result (pixel will appear in original colour in result). 
    # Should isolate the lane in it's original colour while every other pixel in the frame is black(0)
    result = cv2.bitwise_and(img,img,mask=mask) 

    hStack = np.hstack((img,result)) #  Puts img and result side by side in a window for display

    cv2.imshow('hStack',hStack)
    if cv2.waitKey(1) & 0xFF == ord('o'): # break/close when o is pressed 
        break

cap.release() # release resources related to video capture
cv2.destroyAllWindows() # close all windows related to cv2
