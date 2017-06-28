#!/usr/bin/python
# -*- coding: utf-8 -*-
#import datetime (datetime.datetimeと書かないためにfrom)
import pytz
from datetime import datetime

# enable debugging HTML系
from jinja2 import Environment,FileSystemLoader
import cgitb
import cgi
import os
import sys

msg=''
template_filename = './template/world_clock.tpl.html'
country       = []
outputtime    = []
timezone_str  = {"JP":"JST","Nepal":"NPT"}

country.append("JP")
msg+='JP'
country.append("Nepal")
msg+=',Nepal'
msg+=u'をセット'

for cname in country:
    #datetime.fromtimestamp(time.time())と等価
    tempdatail = datetime.today()
    #tempdatail = datetime.fromtimestamp(time.time())
    outputtime.append({"name":timezone_str[cname],"date":tempdatail.strftime("%Y/%m/%d %H:%M:%S")})

cgitb.enable()
env = Environment(loader=FileSystemLoader('./',encoding='utf8'))
tpl = env.get_template(template_filename)
html = tpl.render({'message':msg,"atime":outputtime})
print "Content-Type: text/html;charset=utf-8"
print ""
print html.encode('utf8')
