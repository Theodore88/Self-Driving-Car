# File: utils.py
# Description: This file is designed to implement helper methods that will be used by LaneDetection.py
# Author: Theodore Hoang
import cv2
import numpy as np

def thresholding(img):
    imgTrackbars = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) # convert image from BGR(blue, green, red) color space to HSV color space
    lowerWhite = np.array([0,0,174]) # min values for mask, found using ColorDetection.py 
    upperWhite = np.array([179,59,255]) # max values, found using ColorDetection.py
    mask = cv2.inRange(imgTrackbars,lowerWhite, upperWhite) # Compares each pixel in image to lower and upper threshold values
    # if pixel is within range it's assigned value of 255(white), pixels outside range are assigned 0(black)
    # "mask" is a binary mask, it seperates pixels into white (1) if they are within range and black (0) if not in range
    return(mask)

def warpImage(img, points, width, height, inv=False):
    pts1 = np.float32(points) # original unwarped coordinates
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]]) # Desired coordinates to be warped too 
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2,pts1)

    else:
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(width,height)) # img has been warped to center lane
    return(imgWarp)

def empty(a): # Empty function that is called when trackbars created with cv2.createTrackbar have been manipulated
    pass

def initTrackbars(trackbarVals, wT = 480, hT=240): # Initilizes trackbars
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars",360,240)
    cv2.createTrackbar("Width Max","Trackbars", trackbarVals[0], wT//2, empty) 
    cv2.createTrackbar("Width Min","Trackbars", trackbarVals[1], wT//2, empty) 
    cv2.createTrackbar("Height Max","Trackbars", trackbarVals[2], hT//2, empty) 
    cv2.createTrackbar("Height Min","Trackbars", trackbarVals[3], hT//2, empty)

    # wt//2 so that 2 points stay in left side of centre line and other 2 stay on right side(wT-widthMin and wT-widthMax)

def getTrackbarVals(wT = 480, hT=240):
    widthMax = cv2.getTrackbarPos("Width Max","Trackbars") # Get from HSV window, returns value on trackbar
    heightMax = cv2.getTrackbarPos("Height Max","Trackbars") # Get from HSV window, returns value on trackbar
    widthMin = cv2.getTrackbarPos("Width Min","Trackbars") # Get from HSV window, returns value on trackbar
    heightMin = cv2.getTrackbarPos("Height Min","Trackbars") # Get from HSV window, returns value on trackbar
    points = np.float32([(widthMax,heightMax),(wT- widthMax, heightMax),(widthMin, hT-heightMin),
                         (wT-widthMin,hT-heightMin)]) # Top left, Top right, Bottom left, Bottom right
    return(points)               

def showPoints(img, points): # Draws circles at points on img
    for point in points:
        cv2.circle(img,(int(point[0]),int(point[1])), 15, (0,255,0), cv2.FILLED) # x and y coordinates for 
        # each point , then radius, then color and thickness 
    return(img)

def getHist(img, minPer=0.1, display=False, region = 1):
    if region == 1:
        histValues = np.sum(img,axis=0) # Sum all pixels in each column in img, img is black and white, so white pixels
        # count as 1 and black pixels are value 0, add pixels from left to right
        
    else: # Only looking at bottom 4th portion of histogram
        histValues = np.sum(img[img.shape[0]//region:,:],axis=0)
        """
        The result of img.shape[0]//region is used as the starting index for slicing along 
        the vertical (y) axis of the image. The : after it means to take all the pixels from 
        this starting index to the end of the image. ",:"  means to take all pixels 
        along the horizontal (x) axis. So, img[img.shape[0]//region:,:] selects all pixels 
        from a certain height in the image to the bottom of the image, across all columns.
        """

    maxVal = np.max(histValues)
    minThresh = minPer*maxVal # 20% of max says column is not noise and contains path

    indexArray = [inx for inx , val in enumerate(histValues) if val>=minThresh]
    basePoint = int(np.average(indexArray)) # Given columns that don't have noise, basePoint is the middlest column among columns that contain path 
    if display:
        hist = np.zeros((img.shape[0],img.shape[1],3),np.uint8) # height,width, # ints per value in array 
        # Initiazes each element to [0,0,0], creates an array to represent every pixel in original img
        for inx, intensity in enumerate(histValues):
            cv2.line(hist,(inx,img.shape[0]),(inx,img.shape[0] - intensity//255//region), (255,0,0),1) 
            # Must provide 2 points (start and end points) (inx,img.shape[0]) and (inx,img.shape[0] - intensity/255), divide intensity by 255 because
            # it is to big and won't appear on screen
            # cv2.line will draw lines from bottom of screen to top 
            cv2.circle(hist,(basePoint,img.shape[0]),20,(0,255,255), cv2.FILLED) # Draw basepoint/midpoint
        return(basePoint, hist)
    return(basePoint)
        

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list) # checks if imgArray[0] is present in form
    # of list of lists
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:# If current image and first image
                    # have same shape scale image by given factor
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale) 
                else:
                    # If current image and first image have different shape, resize to match 
                    # first image and apply scale
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR) # convert black and white
        imageBlank = np.zeros((height, width, 3), np.uint8) # Create blank image in same shape as first image
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver