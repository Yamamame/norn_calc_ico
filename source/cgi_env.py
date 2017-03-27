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
cgi.print_environ()
print "</body>"
print "</html>"
