#!/usr/bin/python

# opencv inmport
import cv2, matplotlib
import numpy as np
import matplotlib.pyplot as plt

# enable debugging
from jinja2 import Environment,FileSystemLoader
import cgitb
import cgi
import os
import sys

cgitb.enable()
env = Environment(loader=FileSystemLoader('./',encoding='utf8'))
tpl = env.get_template('opencv_test.tpl.html')
