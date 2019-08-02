#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:57:55 2019

Create a VideoCapture thread and capture a segment of video from webcam

@author: Mike Meyers
"""

#TODO: create start() and stop() methods so that there is only a single file
#TODO: start() trigger will be easy, but how will I know how to stop()?
#TODO: also, this will rewrite files created within the same minute. Need to make
#      unique filenames per recording (global var?)

import time
import datetime
import numpy as np
import cv2
import threading
import traceback

class videoCapture:
    def __init__(self):
        global count
        count = 1
        self.running = False
        self.output = cv2.VideoWriter()
            
    # start() will open the indicated video camera and start recording        
    def start(self, camera=0):
        try:
            FPS = 20.0 #Frames Per Second: change for higher or lower frame rate
            
            # Open VC stream
            self.vc = cv2.VideoCapture(camera)
            
            # Get video resolution
            width = int(self.vc.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print("Resolution is " + str(width) + "x" + str(height)) #TODO: delete later
            
            # Create VideoWriter object
            try:
                vid_cod = cv2.VideoWriter_fourcc('m','p','4','v')
                self.output = cv2.VideoWriter("media/videos/"
                                      + datetime.datetime.now().strftime("%Y_%B_%d_%H%M")
                                        + "_" + str(count) + ".mov",
                                         vid_cod, FPS, (width, height), True)
                print("Video created successfully")
            except: print("Video file not created successfully: "
                          + traceback.format_exc(4))
                
           
            # Add each frame to output video
            currentFrame = 0
            
            self.running = True
            print("Started recording")
        except:
            print("Failed to start recording")
    
        while self.running == True:
            ret, frame = self.vc.read()
            self.output.write(frame)
            currentFrame += 1
            
    # capture.stop() will stop an active capture
    def stop(self):
        self.running = False
         # Close camera and file
        try:
            self.vc.release()
            self.output.release()
            cv2.destroyAllWindows() #TODO: delete later
            print("Recording stopped successfully")
        except:
            print("Failed to stop recording: "
                  + traceback.format_exc(4))
    