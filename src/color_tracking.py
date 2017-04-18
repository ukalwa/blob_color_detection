# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:34:34 2017

@author: ukalwa
"""
import cv2
import numpy as np

def dummy(x):
    pass

def onmouse(event,x,y,flags,params):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        print x,y

point = None
prev_point = None
def get_color_of_object(image, hsv_image):
    global point, prev_point
    win_name = "Object Color identification"
    #easy assigments
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(win_name,onmouse)
    cv2.createTrackbar('H Low', win_name,0,255,dummy)
    cv2.createTrackbar('H High', win_name,11,255,dummy)
    cv2.createTrackbar('S Low', win_name,90,255,dummy)
    cv2.createTrackbar('S High', win_name,255,255,dummy)
    cv2.createTrackbar('V Low', win_name,187,255,dummy)
    cv2.createTrackbar('V High', win_name,255,255,dummy)
    while(1):

        #read trackbar positions for all
        hul=cv2.getTrackbarPos('H Low', win_name)
        huh=cv2.getTrackbarPos('H High', win_name)
        sal=cv2.getTrackbarPos('S Low', win_name)
        sah=cv2.getTrackbarPos('S High', win_name)
        val=cv2.getTrackbarPos('V Low', win_name)
        vah=cv2.getTrackbarPos('V High', win_name)
        #make array for final values
        hsv_low=np.array([hul,sal,val])
        hsv_high=np.array([huh,sah,vah])
    
        #apply the range on a mask
        mask = cv2.inRange(hsv_image,hsv_low, hsv_high)
        res = cv2.bitwise_and(image,image, mask = mask)
#        img = watershed_transform(np.copy(res),mask)
        
#            cv2.rectangle(image_copy,(x,y),(x+w,y+h),(255,0,0),2)
        image_copy,count = detect_object_single_frame(image,res, point, prev_point)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image_copy,'Press q to cancel, c to confirm',(10,50), font, 1,(255,255,0),1)
        cv2.putText(image_copy,'Count %s' %count,(10,100), font, 1,(255,255,0),1)
        cv2.imshow(win_name, image_copy)
        k = cv2.waitKey(5) & 0xFF
        if k == ord('q'):
            ret = False
            break
        if k == ord('c'):
            ret = True
            break
        
    cv2.destroyAllWindows()
    return (ret, hsv_low, hsv_high)

def watershed_transform(image, mask):
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel, iterations = 2)
    
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    markers = cv2.watershed(image,markers)
    image[markers == -1] = [255,0,0]
    return image
    
    
def detect_object_single_frame(image, res, point, prev_point):
    res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    im_mask, cnts, hierarchy = cv2.findContours(res,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    area = np.array([cv2.contourArea(k) for k in cnts])
    cnts = np.array(cnts)[np.logical_and(area>100, area<300)].tolist()
    area = area[np.logical_and(area>100, area<300)]
    
    mask2 = np.zeros(res.shape)
    cv2.drawContours(mask2,cnts,-1,(255,255,255),-1)
    image_copy = np.copy(image)
    if point is not None and point != prev_point:
        for cnt in np.arange(len(cnts)):
            dist = cv2.pointPolygonTest(cnts[cnt],point,True) 
            if dist > 0:
                print area[cnt]
                point = prev_point
    for cnt in np.arange(len(cnts)):
        rect = cv2.boundingRect(cnts[cnt])
        x,y,w,h = rect
        centre_x = x + (w / 2)
        centre_y = y + (h / 2)
#            print w,h
        cv2.rectangle(image_copy,(centre_x-10,centre_y-10),(centre_x+10,centre_y+10),(0,0,0),2)
    return image_copy, len(cnts)
    
def detect_object(image, res):
    res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    im_mask, cnts, hierarchy = cv2.findContours(res,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    area = np.array([cv2.contourArea(k) for k in cnts])
    cnts = np.array(cnts)[np.logical_and(area>100, area<300)].tolist()
    area = area[np.logical_and(area>100, area<300)]
    
    mask2 = np.zeros(res.shape)
    cv2.drawContours(mask2,cnts,-1,(255,255,255),-1)
    image_copy = np.copy(image)
    for cnt in np.arange(len(cnts)):
        rect = cv2.boundingRect(cnts[cnt])
        x,y,w,h = rect
        centre_x = x + (w / 2)
        centre_y = y + (h / 2)
#            print w,h
        cv2.rectangle(image_copy,(centre_x-10,centre_y-10),(centre_x+10,centre_y+10),(0,0,0),2)
    return image_copy, len(cnts)
    
    
    
    
    
    
    
    
    
    
    