#!/usr/bin/python

# enable debugging
from jinja2 import Environment,FileSystemLoader
import cgitb
import cgi
import os
import sys

cgitb.enable()
env = Environment(loader=FileSystemLoader('./',encoding='utf8'))
tpl = env.get_template('cgi_jinja.tpl.html')
vd = {}
v  = []
ak = ['method']

if os.environ['REQUEST_METHOD'] == 'POST' :
    vd['method'] = 'POST'
else :
    vd['method'] = 'GET'

form = cgi.FieldStorage()

for key in form.keys() :
    vd[key]=form[key].value
    ak.append(key)
    v.append({ 'key':key , 'val':form[key].value })

html = tpl.render({'dictkeys':vd,'dictval':v})
print "Content-Type: text/html;charset=utf-8"
print ""
print html.encode('utf8')
