#!/usr/bin/python
#coding: utf-8
#estimate.py
import os
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import warnings
import sys
import csv
#mysql接続関連
#from urllib.parse import urlparse
#from furl import furl
#import mysql.connector
import MySQLdb

db_host     = 'localhost'
db_port     = '3306'
db_user     = 'yama'
db_pass     = 'sYr6nukU'
db_name     = 'altcoins'
db_conn_str = 'mysql://' + db_user + ':' + db_pass
db_conn_str += '@' + db_host  + ':' + db_port + '/' + db_name
#url = urlparse(db_conn_str)
#url = furl(db_conn_str)
# conn = mysql.connector.connect(
conn = MySQLdb.connect(
    host = db_host or 'localhost',
    port = db_port or 3306,
    user = db_user or 'root',
    password = db_pass or '',
    db = db_name
)

#db connect
cursor = conn.cursor()
if conn.is_connected() == False :
  sys.exit()

data_dir = "../../hitbtc/"
data_filename = "trades.csv"
with open(data_dir + data_filename, 'r') as f:
  reader = csv.reader(f)
  # reader = csv.DictReader(f)
  #HEADERを避ける
  #"Date (+09)","Instrument","Trade ID",
  #"Order ID","Side","Quantity","Price",
  #"Volume","Fee","Rebate","Total"
  header = next(reader)

  for row in reader:
    # print row
    # print row[1]
    print header[0] + ':' + row[0] + '\t' +  header[2] + ':' + row[2]
    # print header[0] + ':' + row[header[0]]
    #登録されているかどうか確認
    current_sql  = ' SELECT instrument,quantity,price,volume,fee,rebate,total FROM t_trades'
    current_sql += ' WHERE id=%s '
    cursor.execute(current_sql,row[2])
    data_one = cursor.fetchall()
    print len(data_one)

#get all data
current_sql = 'SELECT instrument,quantity,price,volume,fee,rebate,total FROM t_trades'
cursor.execute(current_sql)
cursor.fetchall()
