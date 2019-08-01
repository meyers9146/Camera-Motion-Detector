#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:58:53 2019

View a video stream and detect any motion.

Done by mixing the tutorial at OpenCV (https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html#background-subtraction)
and Adrian Rosebrock's at https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

@author: Mike Meyers
"""
import argparse
import cv2 as cv
import ffmpeg
import numpy as np
import os
import _thread
import time
import datetime
import videoCapAsync as VideoCaptureAsync
import videoCapture as vc

global j
j = 1

'''
#TODO: Vestigial block of code. Delete later
#Function to determine incoming camera fps
def getFPS(n_frames=500, width=1280, height=720, asynchronous=False): #note: original used "async" which is protected
    if asynchronous:
        camFeed = VideoCaptureAsync(0)
    else:
        camFeed = cv.VideoCapture(0)
    camFeed.set(cv.CAP_PROP_FRAME_WIDTH, width)
    camFeed.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    if asynchronous:
        camFeed.start()
    t0 = time.time()
    i = 0
    while i < n_frames:
        _, frame = cap.read()
        i += 1
    if asynchronous:
        camFeed.stop()
    return int(n_frames / time.time() - t0)
'''

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
        
    # If any contours remain, then motion was detected
    # Create video writer object for recording
    if len(contours[0]) > 0:
        
        # Motion found! Start counter for i at 0
        i = 0
        
        # Create destination folder for recording
        writeToFolder = datetime.datetime.now().strftime("%Y_%B_%d_%H:%M")
        try:
            os.mkdir("media/images/" + writeToFolder)
            os.mkdir("media/videos/" + writeToFolder)
        except:
            pass
        
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
            
            # Write image to file. cv2.imwrite() will return True if successful
            if True == cv.imwrite("media/images/" 
                                  + writeToFolder + "/" 
                                  + "{0:05d}".format(i) + ".jpg", frame):
                i += 1 # increment i for next frame
            else: print("Failed to write image to disk")
        
        #TODO: this is where the ffmpeg call will go
        # Cal ffmpeg to string the images together into a video file
        try:
            if True == ffmpeg.trans_img("media/images/" + writeToFolder + "/00000.jpg",
                             "media/videos/" + writeToFolder,
                             writeToFolder + j + ".avi",
                             "jpg"):
                j += 1
            else: print("Failed to write video to disk: ffmpeg returned False")
        except: print("Failed to write video to disk: Exception thrown")
            
    # Display the resulting frame
    cv.imshow('frame', frame)
    cv.imshow('contour', fgmask)
    cv.startWindowThread()
    
    # Close when user hits 'esc'
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

# When everything done, release the capture
cv.destroyAllWindows()
cap.release()
