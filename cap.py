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
import datetime

# cap: the video stream from the local webcam
# fgbg: the background mask from the local webcam
cap = cv.VideoCapture(0)
fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

# Argument parser creation
# min-area: minimum size of a moving area to be considered motion. Rules out
#          false positives
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type = int, default = 500,
                help = "minimum area size")
args = vars(ap.parse_args())

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
        # Include a timestamp
        cv.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S:%p"),
                   (10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.55, (255, 180, 180), 2)
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    cv.imshow('contour', fgmask)
    cv.startWindowThread()
    
    # Close when user hits 'esc'
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
