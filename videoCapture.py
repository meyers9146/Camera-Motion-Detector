#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:57:55 2019

Create a VideoCapture thread and capture a segment of video from webcam

@author: Mike Meyers
"""

import time
import datetime
import numpy as np
import cv2

class videoCapture:
    def __init__(self):
        pass
    
    def capture(self, camera=0, seconds=10):
        
        FPS = 20.0 #Frames Per Second: change for higher or lower frame rate
        
        # Open VC stream
        vc = cv2.VideoCapture(camera)
        
        # Get video resolution
        width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("Resolution is " + str(width) + "x" + str(height)) #TODO: delete later
        
        # Create VideoWriter object
        try:
            vid_cod = cv2.VideoWriter_fourcc('m','p','4','v')
            output = cv2.VideoWriter("media/videos/" + datetime.datetime.now().strftime("%Y_%B_%d_%H%M") + ".mov",
                                     vid_cod, FPS, (width, height), True)
            print("Video created successfully")
        except: print("Video file not created successfully")
            
        # Determine the total number of frames to be recorded
        frameCount = seconds * FPS
       
        # Add each frame to output video
        currentFrame = 0
        while currentFrame < frameCount:
            ret, frame = vc.read()
            output.write(frame)
            currentFrame += 1
            
        
        # Close camera and file
        vc.release()
        output.release()
        cv2.destroyAllWindows() #TODO: delete later
    
        # Print on success
        #print("Video created successfully")