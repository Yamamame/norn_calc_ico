#!/usr/bin/python
#coding: utf-8
#getdata.py
#hitbtc    : hitbtcからデータを取得するライブラリ
#hitbtc_db : 取得したデータを格納するライブラリ
#参照: https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py
import sys
import os
current_path = os.path.dirname(__file__)
sys.path.append(current_path + '/lib/')
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import warnings
import hitbtc
import hitbtc_db

not_service_symbols = ['DSHBTC','FCNBTC','XMOBTC']

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

for line in f.read().splitlines() :
    if '[mysql]' in line :
        config = 0
    if config >= 0 :
        # 改行コードが除去されないので除去を同時に行う
        strkeydict = line.split('=')
        if 'user' in strkeydict[0] :
            db_user=strkeydict[1]
        if 'password' in strkeydict[0] :
            db_pass=strkeydict[1]
        if 'host' in strkeydict[0] :
          db_host = strkeydict[1]
          
target_rest_url  = "https://api.hitbtc.com"
client = hitbtc.HITBTClient(target_rest_url, api_pub_keys, api_sec_keys)
db_access = hitbtc_db.HITBTCDB(host=db_host,user=db_user,password=db_pass,db_name=db_name)
eth_btc = client.get_symbol('ETHBTC')
address = client.get_address('ETH')     # get eth address for deposit
print('ETH deposit address: "%s"' % address)
# history_trades = client.get_history_trades()
current_symbols="ETHBTC"
used_symbols = db_access.get_used_symbols(1)
for current_symbols in used_symbols :
  print ('ETH deposit address: "%s"' % current_symbols)
  candles = client.get_candles(current_symbols[0])
  print('candles: "%s"' % candles)
  print ('ETH deposit address: "%s"'.format(current_symbols))
  if current_symbols[0] not in not_service_symbols:
    db_access.regist_candles(current_symbols,candles)
