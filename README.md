# Self-Driving-Car
## Description
A self-driving car that operates based on color and lane detection using OpenCV and Raspberry Pi.

## Diagram

![image](https://github.com/Theodore88/Self-Driving-Car/assets/102427757/f864eeb0-a9fb-483e-b48b-d094e032605d)

## Code Summary
- ColorDetection.py: File used for finding color range values needed to detect lane based on color.
- LaneDetection.py: File used for calculating the curve value based on what the car sees.
- Motor.py: Takes the curve value from LaneDetection.py and controls the speed and direction of motors accordingly.
- Webcam.py: Used to return a frame of video captured by the web camera.
- Utils.py: Provides helper functions that are used by LaneDetection.py.
- Main.py: Contains an infinite loop that calls WebCam.py to retrieve a frame from the web camera. This frame is given to LaneDetection.py to retrieve a curve value. After a curve value is obtained, it is sent to Motor.py to move the car based on the curve value.

## Setup Instructions
### Hardware:
Obtain hardware based on the "Components Used" section and connect components according to the "Diagram" section. 

### Software:

1. Make sure Webcam.py is configured to use the correct camera. To do this, run Webcam.py and change the argument of cv2.VideoCapture until the correct camera is used.
2. Run Main.py and change the second argument of getLaneCurve depending on what you would like to be displayed. 
