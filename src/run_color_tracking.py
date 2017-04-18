# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:49:49 2017

@author: ukalwa
"""

import cv2
from color_tracking import get_color_of_object, detect_object
import Tkinter as tk
import tkFileDialog as filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
vid = cv2.VideoCapture(file_path)
bool_read, image = vid.read()
frame = 0
if bool_read:
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    (ret, hsv_low, hsv_high) = get_color_of_object(image, hsv_image)
    if ret:
        mask = cv2.inRange(hsv_image,hsv_low, hsv_high) # Color thresholding
        res = cv2.bitwise_and(image,image, mask = mask)
        image_copy,count = detect_object(image,res)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image_copy,'frame %s Count %s' %(frame,count),(10,50), \
                    font, 1,(255,255,0),1)
        cv2.imshow('Video',image_copy)
        cv2.waitKey(100)
        while vid.isOpened(): # Loop through all frames
            bool_read, image = vid.read()
            if bool_read:
                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_image,hsv_low, hsv_high)
                res = cv2.bitwise_and(image,image, mask = mask)
                image_copy,count = detect_object(image,res)
                frame += 1
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image_copy,'frame %s Count %s' %(frame,count),\
                            (10,50), font, 1,(255,0,0),2)
                cv2.imshow('Video',image_copy)
                cv2.waitKey(100)
            else: # Frame unable to read or reached end of frame
                break
    cv2.destroyAllWindows()
    vid.release()
else:
    print("File not found")


