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
import datetime
import numpy as np
import os
import time
import traceback
from videoCapture import videoCapture

#TODO: Vestigial block of code. Delete later if never used
#Function to determine incoming camera fps
def getFPS(n_frames=500, width=1280, height=720, asynchronous=False): #note: original used "async" which is protected
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
    
# Main portion of the code. Open camera and read input for motion.
# If motion is detected, record it and mark it on the camera feed
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
        
    # If any contours are created, then motion was detected
    if len(contours[0]) > 0:
        
        #TODO: vestigial code
        '''
        # Call videoCapture to capture next 10 seconds of video
        print(videoCapture)
        v = videoCapture()
        
        # Record video in separate thread
        t1 = threading.Thread(target = v.start())
        t1.start()
        '''
        
        #TODO: vestigial code
        '''
        # Create destination folder for recording
        writeToFolder = datetime.datetime.now().strftime("%Y_%B_%d_%H%M")
        count = 1
        try:
            os.mkdir("media/videos/" + writeToFolder)
        except:
            pass
        '''
        
        count = 1
        try:
            FPS = 20.0 #Frames Per Second: change for higher or lower frame rate
        
            # Get video resolution
            width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
            print("Resolution is " + str(width) + "x" + str(height)) #TODO: delete later
            
            # Create VideoWriter object
            try:
                vid_cod = cv.VideoWriter_fourcc('m','p','4','v')
                output = cv.VideoWriter("media/videos/"
                                      + datetime.datetime.now().strftime("%Y_%B_%d_%H%M")
                                        + "_" + str(count) + ".mov",
                                         vid_cod, FPS, (width, height), True)
                print("Video created successfully")
            except: print("Video file not created successfully: "
                          + traceback.format_exc(4))
                
           
            # Add each frame to output video
            currentFrame = 0
            
            running = True
            print("Started recording")
        except:
            print("Failed to start recording")
        
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
        
        output.write(frame)
        currentFrame += 1
    
        '''
        # When contours hits zero, stop recording 
        v.stop()
        '''
        #TODO: this may be in the wrong spot
        #output.release()
        
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    cv.imshow('contour', fgmask)
    cv.startWindowThread()
    
    # Close when user hits 'esc'
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

# When everything done, release the capture
output.release()
cv.destroyAllWindows()
cap.release()
