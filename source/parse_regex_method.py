#!/usr/bin/python
#coding: utf-8
#opencv_testcmd.py
from jinja2 import Environment,FileSystemLoader
import cgitb
import cgi
import os
import sys
from pprint import pprint


template_filename = './template/parse_regex_method.tpl.html'
msg = ''
changetxt = ''
status = ''
# http request parse argument
vd = {}
v  = []
# reciept file
rfile = ''

# HTTP Request
if os.environ['REQUEST_METHOD'] == 'POST' :
    vd['method'] = 'POST'
else :
    vd['method'] = 'GET'

form = cgi.FieldStorage()
formitem = []

for key in form.keys() :
    vd[key]=form.getvalue(key,'')
    if form[key].file:
        # It's an uploaded file; count lines
        formitem = form[key]
        linecount = 0
        while True:
            line = formitem.file.readline()
            if not line: break
            linecount = linecount + 1
            changetxt += line.decode("utf-8")
        v.append({ 'key':'i' + key , 'val':formitem.filename })
    else :
        v.append({ 'key':'e' + key , 'val':form[key].value })

#create HTMl
env = Environment(loader=FileSystemLoader('./',encoding='utf8'))
tpl = env.get_template(template_filename)
html = tpl.render(
    {'message':msg,'changetxt':changetxt,'rect':status,'dictkeys':vd,'dictval':v}
    )
print "Content-Type: text/html;charset=utf-8"
print ""
print html.encode('utf8')
# pprint(formitem, depth=1)
