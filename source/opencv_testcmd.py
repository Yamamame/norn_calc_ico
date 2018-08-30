#!/usr/bin/python
#coding: utf-8
#opencv_testcmd.py
import cv2
import numpy as np
# enable debugging
from jinja2 import Environment,FileSystemLoader
import cgitb
import cgi
import os
import sys

cnt = 0
msg = ''
status = []

filename_list=list()
filename_list.append('5ac8989e-8710-214d-1c2a-008476953a94.jpeg')
filename_list.append('../../Desktop/yoroshikune/FB_IMG_1471088127162.jpg')
filename_list.append('2013-05-18_18-35-27_785.jpg')
filename_list.append('../../Desktop/yoroshikune/1404138199814.jpg')
filename = filename_list[0]
#HAAR分類器の顔検出用の特徴量
git_opencv_path="/home/yama/git/this_work/opencv/"
cascade_list=list()
cascade_list.append(git_opencv_path + "data/haarcascades/haarcascade_frontalface_alt_tree.xml")
cascade_list.append(git_opencv_path + "data/haarcascades/haarcascade_frontalface_alt2.xml")
cascade_list.append(git_opencv_path + "data/haarcascades/haarcascade_frontalface_alt.xml")
cascade_list.append(git_opencv_path + "data/haarcascades/haarcascade_frontalface_default.xml")

cascade_path = cascade_list[0]

faceCascade = cv2.CascadeClassifier(cascade_path)

img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face = faceCascade.detectMultiScale(gray, 1.1, 3)

if len(face) > 0:
	for rect in face:
		cnt+=1
		cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0,255), thickness=2)
#		status[cnt] = tuple(rect[0:2])
		status.append({ 'lt':tuple(rect[0:2]) , 'cube':tuple(rect[2:4])})
else:
	msg = "no face"

cv2.imwrite('detected.jpg', img)
cgitb.enable()
env = Environment(loader=FileSystemLoader('./',encoding='utf8'))
tpl = env.get_template('./template/opencv_test.tpl.html')
html = tpl.render({'filename':filename,'message':msg,'count':cnt,'rect':status})
print ("Content-Type: text/html;charset=utf-8")
print ("")
print (html.encode('utf8'))
