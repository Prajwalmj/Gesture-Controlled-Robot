# -*- coding: utf-8 -*-
"""
Created on Mon May 25 21:03:51 2020

@author: prajwal mj
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import imutils
#import matplotlib.pyplot as plt

#up=1
#down=0
cap=cv2.VideoCapture(0)

def left(cx,cy):
    while(cx>0 and  cx<213 and  cy>=0 and  cy<160):
        #left forward
        print("smooth left")
        cx,cy=get_frame(1)
    while(cx>0 and  cx<213 and  cy>=320 and  cy<480):
        #left reverse
        print("smooth left")
        cx,cy=get_frame(-1)
    while(cx>0 and  cx<=213 and  cy>=160 and  cy<320):
        #hrd left
        print("hard left")
        cx,cy=get_frame(-1)
    


def right(cx,cy):
    while(cx>=426 and  cx<640 and  cy>=0 and  cy<160):
        #right forward
        print("smooth right")
        cx,cy=get_frame(1)
    while(cx>=426 and  cx<640 and  cy>=320 and  cy<480):
        #right reverse
        print("smooth right")
        cx,cy=get_frame(-1)
    while(cx>426 and  cx<=640 and  cy>=160 and  cy<320):
        #hard right
        print("hard right")
        cx,cy=get_frame(-1)

def forward(cx,cy):
    while((cx>=213 and  cx<426 and  cy>=0 and  cy<=160)or( cx==1000 and  cy==1000)):
        #forward
        print("forward")
        cx,cy=get_frame(1)


def reverse(cx,cy):
    while((cx>=213 and  cx<426 and  cy>=320 and  cy<=480) or (cx==-1000 and  cy==-1000)):
        #reverse
        print("reverse")
        cx,cy=get_frame(-1)






def get_centreup(frame):
    cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    try:
            c = max(cnts, key = cv2.contourArea)
            M = cv2.moments(c)
            a = int(M["m10"] / M["m00"])
            b = int(M["m01"] / M["m00"])
    except:
            return(1000,1000)
    return a,b


def get_centredown(frame):
    cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    try:
            c = max(cnts, key = cv2.contourArea)
            M = cv2.moments(c)
            a = int(M["m10"] / M["m00"])
            b = int(M["m01"] / M["m00"])
    except:
            return(-1000,-1000)
    return a,b


def get_centre(frame):
    cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    try:
            c = max(cnts, key = cv2.contourArea)
            M = cv2.moments(c)
            a = int(M["m10"] / M["m00"])
            b = int(M["m01"] / M["m00"])
    except:
            return(2000,2000)
    return a,b




"""
    cv2.line(med1,(213,0),(213,480),(255,255,255),1)
    cv2.line(med1,(426,0),(426,480),(255,255,255),1)
    cv2.line(med1,(0,160),(640,160),(255,255,255),1)
    cv2.line(med1,(0,320),(640,320),(255,255,255),1)
    cv2.imshow('erode',med1)
    k=cv2.waitKey(5) & 0xFF
    if(k==27):
        break
cap.release()
cv2.destroyAllWindows()
"""


def get_frame(status):
 while(True):
  ret,frame=cap.read()
  if(ret):
	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	y_low=np.array([28,153,51])
	y_hi=np.array([36,255,255])
	mask=cv2.inRange(hsv,y_low,y_hi)
	res=cv2.bitwise_and(hsv,frame,mask=mask)
	kernel=np.ones((1,1),np.uint8)
	img_e=cv2.erode(mask,kernel,iterations=5)
	op1=cv2.morphologyEx(img_e,cv2.MORPH_OPEN,kernel)
	med1=cv2.medianBlur(op1,15)
	cv2.imshow('med1',med1)
	if(status==1):
		return get_centreup(med1)
	if(status==0):
		return get_centre(med1)
	if(status==-1):
		return get_centredown(med1)


while(True):
    cx,cy=get_frame(0)
    if(cx>=213 and  cx<426 and  cy>=0 and  cy<=160):
        #go straight
        status=1
        while(True):
            cx,cy=get_frame(1)
            #go straight
            if(cx>=0 and  cx<213 and  cy>=0 and  cy<160):
                #left
                left(cx,cy)
            elif(cx>=426 and  cx<640 and  cy>=0 and  cy<160):
                #right
                right(cx,cy)
            elif((cx>=213 and  cx<426 and  cy>=0 and  cy<=160)or( cx==1000 and  cy==1000)):
                #Forward
                forward(cx,cy)
            else:
                break

    elif(cx>=213 and  cx<426 and  cy>=160 and  cy<320):
        #stop
        status=0
        while(True):
            cx,cy=get_frame(0)
            #go straight
            if(cx>=0 and  cx<213 and  cy>=160 and  cy<320):
                #left
                left(cx,cy)
            elif(cx>=426 and  cx<640 and  cy>=160 and  cy<320):
                #right
                right(cx,cy)
            elif(cx>=213 and  cx<426 and  cy>=160 and  cy<=320):
                #forward
                print("stop")
                pass
            else:
                break

    elif(cx>=213 and  cx<426 and  cy>=320 and  cy<=480):
        #go reverse
        status=-1
        while(True):
            cx,cy=get_frame(-1)
            #go straight
            if(cx>=0 and  cx<213 and  cy>=320 and  cy<480):
                #left
                left(cx,cy)
            if(cx>=426 and  cx<640 and  cy>=320 and  cy<480):
                #right
                right(cx,cy)
            elif((cx>=213 and  cx<426 and  cy>=320 and  cy<=480) or (cx==-1000 and  cy==-1000)):
                #reverse
                reverse(cx,cy)
            else:
                break
    
    k=cv2.waitKey(5) & 0xFF
    if(k==27):
        break
cap.release()
cv2.destroyAllWindows()

