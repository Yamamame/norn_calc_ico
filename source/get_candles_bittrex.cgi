#!/usr/bin/python
#coding: utf-8
#getdata.py
#hitbtc    : hitbtcからデータを取得するライブラリ
#hitbtc_db : 取得したデータを格納するライブラリ
#参照: https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py
import sys
import os
current_path = os.getcwd()
print current_path
sys.path.append('/home/yama/public_html/py_practice/lib/')
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import warnings
import bittrex
import hitbtc_db

debug = 0
merit_threshold = 0.05
aveilable_reserve = 0.75
api_pub_keys=""
api_sec_keys=""
# とりあえずhitbtcで取引しているものだけに
target_currency = ['XDN', 'XMR', 'XMO', 'FCN', 'DSH', 'BTG']
data_dir = "/home/yama/Documents/bittrex/"
f = open(data_dir + 'apikey.txt', 'r')
for line in f :
    strkeydict = line.split(None)
    if 'API' in strkeydict[0] :
      api_pub_keys = strkeydict[1]
    else :
      api_sec_keys = strkeydict[1]
# db接続情報
f = open(data_dir + 'dbconfig.txt', 'r')
for line in f :
    strkeydict = line.split(None)
    if 'host' == strkeydict[0] :
        db_host = strkeydict[1]
    elif 'port' == strkeydict[0] :
        db_port = int(strkeydict[1])
    elif 'user' == strkeydict[0] :
        db_user = strkeydict[1]
    elif 'password' == strkeydict[0] :
        db_pass = strkeydict[1]
    elif 'db_name' == strkeydict[0] :
        db_name = strkeydict[1]

client = bittrex.BITTREXClient(api_pub_keys, api_sec_keys)
marksum = client.get_getmarketsummaries()
amark = client.get_ticker()
print(" ^-^{} ".format(amark))
db_access = hitbtc_db.HITBTCDB(
    host=db_host, port=db_port, user=db_user, password=db_pass, db_name=db_name, mode='bittrex')

print(" {} ".format(marksum['message']))
for curr_summary in marksum['result']:
    # print(" {} ".format(curr_summary))
    for currency in target_currency :
        if currency in curr_summary['MarketName'] :
            print("aaa {} ".format(curr_summary))
            db_access.regist_candles(curr_summary['MarketName'], curr_summary,debug=debug)
