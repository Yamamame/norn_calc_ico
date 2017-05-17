from jinja2 import Environment,FileSystemLoader
import cgitb
import cgi
import os
import sys

template_filename = './template/parse_regex_method.ptl.html'


html = tpl.render({'filename':filename,'message':msg,'count':cnt,'rect':status})
print "Content-Type: text/html;charset=utf-8"
print ""
print html.encode('utf8')
