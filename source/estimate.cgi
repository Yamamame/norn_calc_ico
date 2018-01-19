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
db_port     = 3306
db_user     = 'yama'
db_pass     = 'sYr6nukU'
db_name     = 'altcoins'
db_conn_str = 'mysql://' + db_user + ':' + db_pass
#url = urlparse(db_conn_str)
#url = furl(db_conn_str)
# conn = mysql.connector.connect(
conn = MySQLdb.connect( host = db_host,
  port = db_port,
  user = db_user,
  passwd = db_pass,
  db = db_name,
)

#db connect
cursor = conn.cursor()
# if conn.is_connected() == False :
#   sys.exit()
try:
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
      row[8] = str(float(row[8]) - float(row[9]))
      print header[0] + ':' + row[0] + '\t' +  header[2] + ':' + row[2] + ':' + row[8] + ':' + str(float(row[9]))
      # print header[0] + ':' + row[header[0]]
      #登録されているかどうか確認
      current_sql  = ' SELECT instrument,quantity,price,volume,fee,rebate,total FROM t_trades'
      current_sql += ' WHERE id=%s '
      placehold = (row[2],)
      cursor.execute(current_sql,placehold)
      data_one = cursor.fetchall()
      print len(data_one)
      #rebateは-のfeeという考え方に変更
      #
      if len(data_one) == 0:
        current_sql  = ' INSERT INTO t_trades '
        current_sql += ' (exec_date,instrument,id'
        current_sql += ' ,order_id,side,quantity,price'
        current_sql += ' ,volume,fee,total)'
        current_sql += ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        placehold = (
          row[0],row[1],row[2],
          row[3],row[4],row[5],row[6],
          row[7],row[8],row[9],row[10],
        )
        # cursor.execute(current_sql,placehold)
        print 'INSERT OK'
      else :
        # current_sql  = ' UPDATE t_trades SET '
        # current_sql += ' exec_date = %s,instrument=%s'
        # current_sql += ' ,order_id=%s,side=%s,quantity=%s,price=%s'
        # current_sql += ' ,volume=%s,fee=%s,rebate=%s,total=%s '
        # current_sql += ' WHERE id=%s '
        # placehold = (
        #   row[0],row[1],
        #   row[3],row[4],row[5],row[6],
        #   row[7],row[8],row[9],row[10],
        #   row[2],
        # )
        current_sql  = ' UPDATE t_trades SET '
        # current_sql += ' exec_date = %s,instrument=%s'
        # current_sql += ' ,order_id=%s,side=%s,quantity=%s,price=%s'
        # current_sql += ' ,volume=%s,fee=%s,rebate=%s,total=%s '
        current_sql += ' volume=%s,total=%s,uptime=now() '
        current_sql += ' WHERE id=%s '
        placehold = (
          # row[0],row[1],
          # row[3],row[4],row[5],row[6],
          # row[7],row[8],row[9],row[10],
          row[7],row[10],
          row[2],
        )
        cursor.execute(current_sql,placehold)
        print 'UPDATE OK'
      conn.commit()
  #get all data
  current_sql = 'SELECT instrument,quantity,price,volume,fee,rebate,total FROM t_trades'
  cursor.execute(current_sql)
  cursor.fetchall()

finally:
  cursor.close()
  conn.close()
