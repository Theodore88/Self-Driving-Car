# File: LaneDetection.py
# Description: This file is designed to implement getLaneCurve(). getLaneCurve takes in a img which contains a lane and calcualtes the curvature
# of that lane and returns it. getLaneCurve() also takes in an argument which determines whichs views of the car is to be displayed
# be displayed
# Author: Theodore Hoang

import cv2
import numpy as np
import utils
curveList = []
avgVal = 10 # keeps curveList at max len 10
def getLaneCurve(img, display = 2): 
    mask = utils.thresholding(img) # send in image and get returned the mask of image based of HSV bounds found in ColorDetection.py
    height, width, channel = img.shape # return dimensions of image/what camera sees
    points = utils.getTrackbarVals() # Retrieve points in image that will be used in warping image
    imgWarped = utils.warpImage(mask, points, width, height) # Warp image so that lane can be view from a birdseye view
    imgCpy = img.copy()
    imgResult = img.copy()
    imgWarpPoints = utils.showPoints(imgCpy, points) # Creates displays image with points displayed on image

    """
    Curve value is determined by getting the indexes of all columns of pixels that pass a certain
    threshold. The mean of all indexes is taken. The index that marks the center of the img is subtracted from the mean to get curve value
    A negative curve value will result in a left turn
    """
    # POINTS ARE ALL INDEXES OF COLUMNS
    middlePoint, imgHist = utils.getHist(imgWarped,minPer=0.5,display=True, region=4) # Find middle of path and get histogram of 
    # bottom part of image (first 4th of image)
    curveAveragepoint, imgHist = utils.getHist(imgWarped, minPer=0.9, display=True) # Gets historgram of whole img
    # curveAveragePoint = average column among columns with no noise

    curveRaw = curveAveragepoint - middlePoint # Calculates curve value before normalizing

    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList)) # Average of curve values in curve list, do this instead of looking
    # at individual values so that we can avoid big jumps in curve values

    if display != 0: # Display image with visulization of lane detection
        imgInvWarp = utils.warpImage(imgWarped, points, width, height, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR) # change from black and white to colored img
        imgInvWarp[0:height // 3, 0:width] = 0,0,0 # Set top one third of image black 
        imgLaneColor = np.zeros_like(img) # Create image same as "img" but, make pixels all black 
        imgLaneColor[:] = 0,255,0 # set all pixels to green in imgLaneColor
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor) # Apply green to all non black values in imgInvWarp
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0) # Move green lane color to lane in original image
        midY = 450
        cv2.putText(imgResult,str(curve),((width//2)-40,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3) # Display curve value as text on screen
        cv2.line(imgResult,(width//2,midY),(width//2+(curve*3),midY),(255,0,255),5) # Borders lane in magenta
        cv2.line(imgResult, ((width // 2 + (curve * 3)), midY-25), (width // 2 + (curve * 3), midY+25), (0, 255, 0), 5) # Highlights lane in green


        if display == 2:
            imgStacked = utils.stackImages(0.7,([img,imgWarpPoints,imgWarped], # Function that will stack images side by side
                                                [imgHist,imgLaneColor,imgResult]))
            cv2.imshow('ImageStack',imgStacked) # Shows all images
        elif display == 1:
            cv2.imshow('Result',imgResult) # Just shows result

    #NORMALIZATION    
    curve = curve/100 # scale down curve value
    if curve>1: curve == 1
    if curve<1: curve == -1
    # 1 and -1 are max and min, everything else should fall between the two 
    return curve


if __name__ == '__main__':
    # Used in the testing of LaneDetection.py
    cap = cv2.VideoCapture('IMG_0291.MOV') 
    utils.initTrackbars([122,59,120,57])
    frameCounter = 0
    while True: # Initilize infinite loop to read frames from video
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter: # when video has reached end loop back to beggining 
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter = 0

        success,img = cap.read() 
        img = cv2.resize(img,(480,240)) # change dimensions of image
        curve = getLaneCurve(img, display=2)
        cv2.waitKey(20) # delay 20 ms
