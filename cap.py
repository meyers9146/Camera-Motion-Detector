#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:58:53 2019

View a video stream and detect any motion.

Done by mixing the tutorial at OpenCV (https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html#background-subtraction)
and Adrian Rosebrock's at https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

@author: Mike Meyers
"""

import numpy as np
import cv2 as cv
import argparse
import time

# cap: the video stream from the local webcam
# fgbg: the background mask from the local webcam
cap = cv.VideoCapture(0)
fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
#time.sleep(10.0) #TODO: let it warm up?

'''
while True:
    ret, frame = cap.read()
    
    fgmask = fgbg.apply(frame)
    cv.imshow("window", fgmask)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
'''      


# Argument parser creation
# min-area: minimum size of a moving area to be considered motion. Rules out
#          false positives
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type = int, default = 500,
                help = "minimum area size")
args = vars(ap.parse_args())

#TODO: the tutorial page has a VideoStream object here. May need to add it in
#TODO: If using the direct VideoCapture doesn't work

# If the capture cannot retrieve an image, report an issue with camera
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Create background mask by subtracting non-moving pixels from frame
    fgmask = fgbg.apply(frame)
    
    
    # Grab contours from masked image
    contours = cv.findContours(fgmask.copy(), cv.RETR_EXTERNAL,
                               cv.CHAIN_APPROX_SIMPLE)
    # cv2.findContours returns a tuple. The first item in this tuple is our
    # list of contours. Iterate over the list of contours to process.
    for contour in contours[0]:
        # Ignore false positives
        if cv.contourArea(contour) < args["min_area"]:
            continue
        
        # Compute the bounding box for the contour and draw it on the frame
        (x, y, w, h) = cv.boundingRect(contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    cv.startWindowThread()
    
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
