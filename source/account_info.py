#!/usr/bin/python
#coding: utf-8
#account_info.py
#hitbtc    : hitbtcからデータを取得するライブラリ
#hitbtc_db : 取得したデータを格納するライブラリ
#参照: https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py
import sys
import os
current_path = os.getcwd()
sys.path.append('/home/yama/public_html/py_practice/lib/')
import numpy as np
import warnings
import hitbtc
import hitbtc_db
from jinja2 import Environment,FileSystemLoader
import cgitb

data_dir = "/home/yama/hitbtc/"
f = open(data_dir + 'apikey.txt', 'r')
for line in f :
    strkeydict = line.split(None)
    if 'API' in strkeydict[0] :
      api_pub_keys = strkeydict[1]
    else :
      api_sec_keys = strkeydict[1]
target_rest_url  = "https://api.hitbtc.com"
client = hitbtc.HITBTClient(target_rest_url, api_pub_keys, api_sec_keys)
db_access = hitbtc_db.HITBTCDB()
eth_btc = client.get_symbol('ETHBTC')
address = client.get_address('ETH')     # get eth address for deposit
print('ETH deposit address: "%s"' % address)
# history_trades = client.get_history_trades()
current_symbols="ETHBTC"
# main accountで表示される値の表示
account_balance = client.get_account_balance()
# tradingで表示される値の表示
trading_balance = client.get_trading_balance()
all_balance = {}

for current_symbols in account_balance :
    if float(current_symbols['available']) > 0.0 or float(current_symbols['reserved']) > 0.0 :
        # print("{}".format(current_symbols))
        if current_symbols['currency'] not in all_balance :
            all_balance[current_symbols['currency']] = {}
        all_balance[current_symbols['currency']]['account'] = current_symbols

for current_symbols in trading_balance :
    if float(current_symbols['available']) > 0.0 or float(current_symbols['reserved']) > 0.0 :
        # print("{}".format(current_symbols))
        if current_symbols['currency'] not in all_balance :
            all_balance[current_symbols['currency']] = {}
        all_balance[current_symbols['currency']]['trading'] = current_symbols


for current_symbols in all_balance :
    print("symbol : {0}".format(current_symbols))
    if 'account' in all_balance[current_symbols] :
        print("account : {}".format(all_balance[current_symbols]['account']))
    if 'trading' in all_balance[current_symbols] :
        print("trading : {}".format(all_balance[current_symbols]['trading']))

# 画面表示
# template_filename = './template/account_info.tpl.html'
# message = "test中"
# cgitb.enable()
# env = Environment(loader=FileSystemLoader('./',encoding='utf8'))
# tpl = env.get_template(template_filename)
# html = tpl.render({'message':message,'all_balance':all_balance})
# print "Content-Type: text/html;charset=utf-8"
# print ""
# print html.encode('utf8')
