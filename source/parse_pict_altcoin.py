#!/usr/bin/python
#coding: utf-8
#opencv_testcmd.py
from jinja2 import Environment,FileSystemLoader
import cgitb
import cgi
import os
import sys
from pprint import pprint
#analyze picture
import cv2

template_filename = './template/parse_pict_altcoin.html'
file_save_dir     = './altcoin/'
msg = ''
changetxt = ''
status = ''
# http request parse argument
vd = {}
v  = []
# reciept file
rfile = ''

#HAAR分類器の顔検出用の特徴量
cascade_list=list()
cascade_list.append("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt_tree.xml")
cascade_list.append("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")
cascade_list.append("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
cascade_list.append("/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml")
cascade_path = cascade_list[0]

faceCascade = cv2.CascadeClassifier(cascade_path)

#画像保存用のディレクトリ作成
if os.path.isdir(file_save_dir) == False :
    os.mkdir(file_save_dir)

# HTTP Request
if os.environ['REQUEST_METHOD'] == 'POST' :
    vd['method'] = 'POST'
else :
    vd['method'] = 'GET'

form = cgi.FieldStorage()
formitem = []

for key in form.keys() :
    vd[key]=form.getvalue(key,'')
    item_error_msg = ''
    if form[key].file:
        # It's an uploaded file; count lines
        formitem = form[key]
        img = cv2.imread(formitem.filename, cv2.IMREAD_UNCHANGED)
        if img is None:
            if os.path.exists(formitem.filename) == False :
                item_error_msg = formitem.filename +  ' file not found !!'
            else :
                item_error_msg = formitem.filename +  ' Is Error !!'
        else :
            #pict processing
            height = img.shape[0]
            width = img.shape[1]
            cv2.rectangle(img, (2,10), (width - 2, height - 2), (0, 0,255), thickness=2)
            cv2.imwrite(file_save_dir + formitem.filename, img)
        v.append({ 'key':'i' + key , 'val':formitem.filename , 'err':item_error_msg })
    else :
        item_error_msg = 'File not found !!'
        v.append({ 'key':'e' + key , 'val':form[key].value , 'err':item_error_msg })



#create HTMl
env = Environment(loader=FileSystemLoader('./',encoding='utf8'))
tpl = env.get_template(template_filename)
html = tpl.render(
    {'message':msg,'changetxt':changetxt,'rect':status,'dictkeys':vd,'dictval':v}
    )
print ("Content-Type: text/html;charset=utf-8")
print ("")
print (html.encode('utf8'))
# pprint(formitem, depth=1)
