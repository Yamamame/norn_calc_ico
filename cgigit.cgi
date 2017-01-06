#!/usr/bin/python

# enable debugging
import cgitb
import cgi
cgitb.enable()

print "Content-Type: text/html;charset=utf-8"
print ""
print "<html>"
print "<head><title>env</title></head>"
print "<body>"
print "<p>ssh://norn@133.242.224.125:34897/var/git/BookMaker.git</p>"
print "</body>"
print "</html>"
