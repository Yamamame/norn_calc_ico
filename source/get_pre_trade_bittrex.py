#!/usr/bin/python3
#coding: utf-8
#get_pre_trade.py
#hitbtc    : hitbtcからデータを取得するライブラリ
#hitbtc_db : 取得したデータを格納するライブラリ
#参照: https://github.com/hitbtc-com/hitbtc-api/blob/master/example_rest.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/lib/')
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import warnings
import re
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
            db_access.regist_candles(curr_summary['MarketName'], curr_summary,debug=1)

# for trading_row in trading_balance :
#   if float(trading_row['available']) == 0.0 :
#       continue
#   cur_currency = trading_row['currency']
#   print( '!==============================={0}================================='.format(cur_currency))
#   print( '!=== {0} ==='.format(trading_row) )
#   print( '!===================================================================')
#   pre_trades = db_access.pre_trade_value(cur_currency)
#   for data_row in pre_trades :
#     trade_price    = data_row[2]
#     now_quantity   = trade_price
#     now_instrument = str(data_row[0])
#     if debug == 1 :
#         print( 'instrument: "{0}" side : "{3:5}" price : "{1: 4.8f}"  quantity : "{2: 4.8f}" '.format(now_instrument,data_row[1],trade_price,data_row[3]))
#     res = db_access.get_recently_price(str(data_row[0]))
#     for res_row in res :
#         trading_price = 0.0
#         trading_merit = 0.0
#         diff_val = 0.0
#         for_side = ""
#         # symbols,min,max,open,close,volume,timestamp
#         # print('instrument: "%s" ' % (res_row[0]))
#         if (data_row[3] == "sell" and re.match(".*" + cur_currency + "$",now_instrument)):
#             for_side = "for buy"
#             diff_val =  data_row[1] - (res_row[2] * (1 + merit_threshold))
#             trading_price = (trade_price ) * (data_row[1] - (res_row[1] * (1 + merit_threshold)))
#             trading_merit = (trade_price ) * (data_row[1] - (res_row[1] * (1 + merit_threshold)))
#             # 後ろ側にinstrumentがあった場合は価格は変動する方の価格になる
#             now_quantity = ((res_row[1] + res_row[2]) / 2) * trade_price
#         elif (data_row[3] == "buy" and re.match("^" + cur_currency + ".*",now_instrument)):
#             trading_merit = 0
#             trading_price = 0
#         else :
#             for_side = "for sell"
#             diff_val = (res_row[1] * (1 - merit_threshold))- data_row[1]
#             trading_price = (trade_price ) * ((res_row[1] * (1 - merit_threshold))- data_row[1])
#             trading_merit = (trade_price ) * ((res_row[1] * (1 - merit_threshold))- data_row[1])
#         if debug == 1 :
#             print('instrument: "{0}" min   : "{1: 4.8f}"  max  : "{2: 4.8f}"'.format(res_row[0],res_row[1],res_row[2],))
#             print(' ------------> {0:8} diff : {1: 4.8f} merit {2: 4.8f}"'.format(for_side,diff_val,trading_merit))
#         if trading_merit > 0.0 and (float(trading_row['available']) * aveilable_reserve) > now_quantity:
#             print( '!=^=^=^=^==============trading==={0}={1}================================='.format(for_side,cur_currency))
#             print( '!=^= instrument: {0} quantity : {1: 4.8f} aveilable : {2} recently trade : {3: 4.8f} ==='.format(
#                 now_instrument,trade_price,trading_row['available'],data_row[1]
#             ))
#             print('!=^= min   : "{0: 4.8f}"  max  : "{1: 4.8f}"  trading merit {2: 4.8f} ==='.format(res_row[1],res_row[2],trading_price))
#             print ("!------------> timestamp {0:%Y-%m-%d %H:%M:%S}".format(res_row[6]))
#             print( '!=^=^=^=^===========================================================')
