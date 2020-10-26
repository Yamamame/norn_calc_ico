#!/usr/bin/python
#coding: utf-8
#getdata.py
#hitbtc    : hitbtcからデータを取得するライブラリ
#hitbtc_db : 取得したデータを格納するライブラリ
#参照: https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py
import sys
import os
current_path = os.getcwd()
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/lib/')
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import warnings
import hitbtc
import hitbtc_db

data_dir = os.environ['HOME'] + '/hitbtc/'
f = open(data_dir + 'apikey.txt', 'r')
for line in f :
    strkeydict = line.split(None)
    if 'API' in strkeydict[0] :
      api_pub_keys = strkeydict[1]
    else :
      api_sec_keys = strkeydict[1]

f = open(data_dir + '.my.cnf', 'r')
db_host="localhost"
db_user=""
db_pass=""
db_name="altcoins"
config = -1

for line in f :
    if '[mysql]' in line:
        config = 0
    if config >= 0 :
        strkeydict = line.split('=')
        if 'user' in strkeydict[0] :
            db_user=strkeydict[1]
        if 'password' in strkeydict[0] :
            db_pass=strkeydict[1]
        if 'host' in strkeydict[0] :
          db_host = strkeydict[1]

target_rest_url  = "https://api.hitbtc.com"
client = hitbtc.HITBTClient(target_rest_url, api_pub_keys, api_sec_keys)
eth_btc = client.get_symbol('ETHBTC')
address = client.get_address('ETH')     # get eth address for deposit
print('ETH deposit address: "%s"' % address)
# history_trades = client.get_history_trades()
history_trades = client.get_history_trades_by_a_month()
# print('history trades: "%s"' % history_trades)
db_access = hitbtc_db.HITBTCDB(host=db_host,user=db_user,password=db_pass,db_name=db_name)
db_access.regist_dict(history_trades)
