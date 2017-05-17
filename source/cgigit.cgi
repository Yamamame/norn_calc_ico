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
print "<p>ssh://yama@153.127.203.136:9574/home/yama/git/practice_py/</p>"
print "<p>ssh://norn@153.127.203.136:9574/home/norn/git/nisshin.git/</p>"
print "<p>ssh://yama@192.168.192.103:9574/home/yama/git/eae.git</p>"
print "<p>ssh://yama@153.127.203.136:9574/home/yama/git/oomori.git/</p>"
print "<p>ssh://norn@153.127.203.136:9574/home/norn/git/mumu.git/</p>"
print "<p>ssh://norn@153.127.203.136:9574/home/norn/git/calc_sample.git/</p>"
print "</body>"
print "</html>"
