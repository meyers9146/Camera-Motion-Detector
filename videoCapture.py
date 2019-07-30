#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:57:55 2019

Create a VideoCapture thread and capture a segment of video from webcam

@author: Mike Meyers
"""

import time
import datetime
import cv2

def videoCapture(camera=0, seconds=10):
    
    FPS = 20.0 #Frames Per Second: change for higher or lower frame rate
    
    # Open VC stream
    vc = cv2.VideoCapture(camera)
    
    # Get video resolution
    width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Resolution is " + str(width) + "x" + str(height)) #TODO: delete later
    
    # Create VideoWriter object
    vid_cod = cv2.VideoWriter_fourcc(*"MPEG")
    output = cv2.VideoWriter("media/video/" + time.strftime("%d-%m-%Y_%X"),
                             vid_cod, FPS, (width, height))
    
    # Determine the total number of frames to be recorded
    frameCount = seconds * FPS
    
    # Add each frame to output video
    currentFrame = 0
    while currentFrame < frameCount:
        ret, frame = vc.read()
        cv2.imshow("testvideo", frame) #TODO: delete later
        output.write(frame)
        currentFrame += 1
        
    cv2.destroyAllWindows() #TODO: delete later
    
    # Close camera and file
    vc.release()
    output.release()
    
    # Print on success
    print("Video created successfully")