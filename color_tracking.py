# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:49:49 2017

@author: ukalwa
"""

import cv2
from get_color_of_object import get_color_of_object, detect_object

vid = cv2.VideoCapture(r'C:\Users\ukalwa\Downloads\1.mp4')
bool_read, image = vid.read()
counter = 0
frame = 0
if bool_read:
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    (ret, hsv_low, hsv_high) = get_color_of_object(image, hsv_image)
    if ret:
        mask = cv2.inRange(hsv_image,hsv_low, hsv_high)
        res = cv2.bitwise_and(image,image, mask = mask)
        image_copy,count = detect_object(image,res)
        counter = count + counter
        while vid.isOpened():
            bool_read, image = vid.read()
            if bool_read:
                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_image,hsv_low, hsv_high)
                res = cv2.bitwise_and(image,image, mask = mask)
                image_copy,count = detect_object(image,res)
                counter = count + counter
                frame += 1
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image_copy,'frame %s Count %s' %(frame,counter),(10,50), font, 1,(255,255,0),1)
                cv2.imshow('image',image_copy)
                cv2.waitKey(100)
            else:
                break
else:
    print("File not found")

print counter
cv2.destroyAllWindows()
vid.release()
