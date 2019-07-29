#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:58:53 2019

@author: Mike
"""

import numpy as np
import cv2 as cv

#cap: the video stream from the local webcam
#fgbg: the background mask from the local webcam
cap = cv.VideoCapture(0)
fgbg = cv.bgsegm.createBackgroundSubtractorGMG()

#If the capture cannot retrieve an image, report an issue with camera
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
    
    # Display the resulting frame
    cv.imshow('frame', fgmask)
    cv.startWindowThread()
    
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
