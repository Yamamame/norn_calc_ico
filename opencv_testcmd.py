#!/usr/bin/python
#coding: utf-8

import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img = cv2.imread('../../Desktop/1404138199814.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face = faceCascade.detectMultiScale(gray, 1.1, 3)

if len(face) > 0:
	for rect in face:
		cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0,255), thickness=2)
else:
	print "no face"

cv2.imwrite('detected.jpg', img)