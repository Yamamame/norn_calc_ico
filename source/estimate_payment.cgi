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
  data_filename = "payment_history.csv"
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
      current_sql  = ' SELECT exec_date,operation_id_1,operation_id_2 FROM payment_history'
      current_sql += ' WHERE operation_id_1=%s AND operation_id_2=%s AND operation_id_3=%s '
      current_sql += ' AND operation_id_4=%s AND operation_id_5=%s ;'
      placehold = (
        row[1].split("-")[0], row[1].split("-")[1], row[1].split("-")[2],
        row[1].split("-")[3], row[1].split("-")[4],
      )
      cursor.execute(current_sql,placehold)
      data_one = cursor.fetchall()
      print len(data_one)
      #
      if len(data_one) == 0:
        current_sql  = ' INSERT INTO payment_history '
        current_sql += ' (exec_date,operation_id_1,operation_id_2,operation_id_3'
        current_sql += ' ,operation_id_4,operation_id_5,type,amount'
        current_sql += ' ,t_hash,main_balance,currency,uptime)'
        current_sql += ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now());'
        placehold = (
          row[0], row[1].split("-")[0], row[1].split("-")[1], row[1].split("-")[2],
          row[1].split("-")[3], row[1].split("-")[4], row[2], row[3],
          row[4], row[5], row[6],
        )
        cursor.execute(current_sql,placehold)
        print 'INSERT OK'
      else :
        current_sql  = ' UPDATE payment_history SET '
        current_sql += ' exec_date = %s '
        current_sql += ' ,type=%s,amount=%s'
        current_sql += ' ,t_hash=%s,main_balance=%s,currency=%s,uptime=now() '
        current_sql += ' WHERE operation_id_1=%s AND operation_id_2=%s AND operation_id_3=%s '
        current_sql += ' AND operation_id_4=%s AND operation_id_5=%s ;'
        placehold = (
          row[0],
          row[2],row[3],
          row[4],row[5],row[6],
          row[1].split("-")[0], row[1].split("-")[1], row[1].split("-")[2],
          row[1].split("-")[3], row[1].split("-")[4]
        )
        # current_sql  = ' UPDATE payment_history SET '
        # current_sql += ' volume=%s,rebate=%s,total=%s '
        # current_sql += ' WHERE id=%s '
        # placehold = (
        #   row[7],row[9],row[10],
        #   row[2],
        # )
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
