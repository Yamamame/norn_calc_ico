#!/usr/bin/python
#coding: utf-8
#opencv_testcmd.py
from jinja2 import Environment,FileSystemLoader
import cgitb
import cgi
import os
import sys

template_filename = './template/parse_regex_method.tpl.html'
msg = ''
changetxt = ''
status = ''
#create HTMl
env = Environment(loader=FileSystemLoader('./',encoding='utf8'))
tpl = env.get_template(template_filename)
html = tpl.render({'message':msg,'changetxt':changetxt,'rect':status})
print "Content-Type: text/html;charset=utf-8"
print ""
print html.encode('utf8')
