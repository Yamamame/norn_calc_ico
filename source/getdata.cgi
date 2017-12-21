#!/usr/bin/python
#coding: utf-8
#getdata.py
#hitbtc    : hitbtcからデータを取得するライブラリ
#hitbtc_db : 取得したデータを格納するライブラリ
#参照: https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py
import sys
sys.path.append('./lib/')
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import warnings
import hitbtc
import hitbtc_db

data_dir = " ../../hitbtc/"
api_pub_keys = "a98a09ed69db5faa37faeeeb47af4967"
api_sec_keys = "8066b231b7b50e626b020ed5c593170b"
target_rest_url  = "https://api.hitbtc.com"
client = hitbtc.HITBTClient(target_rest_url, api_pub_keys, api_sec_keys)
eth_btc = client.get_symbol('ETHBTC')
address = client.get_address('ETH')     # get eth address for deposit
print('ETH deposit address: "%s"' % address)
# history_trades = client.get_history_trades()
history_trades = client.get_history_trades_by_a_month()
print('history trades: "%s"' % history_trades)
db_access = hitbtc_db.HITBTCDB()
db_access.regist_dict(history_trades)