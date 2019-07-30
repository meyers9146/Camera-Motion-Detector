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
    
    # Create VideoWriter object
    vid_cod = cv2.VideoWriter_fourcc(*"XVID")
    output = cv2.VideoWriter("videos/cam_video.mp4", vid_cod, FPS, (640,480))
    
    # Determine the total number of frames to be recorded
    frameCount = seconds * FPS
    
    # Add each frame to output video
    for frame in frameCount:
        ret, frame = vc.read()
        output.write(frame)
    
    # Close camera and file
    vc.release()
    output.release()
    