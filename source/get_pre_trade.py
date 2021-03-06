#!/usr/bin/python
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
import hitbtc
import hitbtc_db


debug = 1
merit_threshold = 0.04
aveilable_reserve = 0.75
hundredth_percent_symbols = ['XDNBTC', ]
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
eth_btc = client.get_symbol('ETHBTC')
address = client.get_address('ETH')     # get eth address for deposit
trading_balance = client.get_trading_balance()
db_access = hitbtc_db.HITBTCDB()
for trading_row in trading_balance :
    if float(trading_row['available']) == 0.0 :
        continue
    cur_currency = trading_row['currency']
    print( '!==============================={0}================================='.format(cur_currency))
    print( '!=== {0} ==='.format(trading_row) )
    print( '!===================================================================')
    pre_trades = db_access.pre_trade_value(cur_currency)
    for data_row in pre_trades :
        now_instrument = str(data_row[0])
        if now_instrument in hundredth_percent_symbols :
            trade_price = (data_row[2] * 0.01)
        else :
            trade_price = (data_row[2] * 1)
        now_quantity   = trade_price
        if debug == 1 :
            print( 'instrument: "{0}" side : "{3:5}" price : "{1: 4.10f}"  quantity : "{2: 4.10f}" '.format(now_instrument,data_row[1],trade_price,data_row[3]))
        res = db_access.get_recently_price(str(data_row[0]))
        for res_row in res :
            trading_price = 0.0
            trading_merit = 0.0
            expected_value = 0.0
            diff_val = 0.0
            for_side = ""
            # symbols,min,max,open,close,volume,timestamp
            # print('instrument: "%s" ' % (res_row[0]))
            if (data_row[3] == "sell" and re.match(".*" + cur_currency + "$",now_instrument)):
                for_side = "for buy"
                diff_val =  data_row[1] - (res_row[2] * (1 + merit_threshold))
                trading_price = (trade_price ) * (data_row[1] - (res_row[1] * (1 + merit_threshold)))
                trading_merit = (trade_price ) * (data_row[1] - (res_row[1] * (1 + merit_threshold)))
                expected_value = (res_row[1] * (1 + merit_threshold))
                # 後ろ側にinstrumentがあった場合は価格は変動する方の価格になる
                now_quantity = ((res_row[1] + res_row[2]) / 2) * trade_price
            elif (data_row[3] == "buy" and re.match("^" + cur_currency + ".*",now_instrument)):
                trading_merit = 0
                trading_price = 0
                expected_value = 0
            else :
                for_side = "for sell"
                diff_val = (res_row[1] * (1 - merit_threshold))- data_row[1]
                trading_price = (trade_price ) * ((res_row[1] * (1 - merit_threshold))- data_row[1])
                trading_merit = (trade_price ) * ((res_row[1] * (1 - merit_threshold))- data_row[1])
                expected_value = (res_row[1] * (1 - merit_threshold))
            if debug == 1 :
                print('instrument: "{0}" min   : "{1: 4.10f}"  max  : "{2: 4.10f}"'.format(res_row[0],res_row[1],res_row[2],))
                print(' ------------> {0:8} diff : {1: 4.10f} merit {2: 4.10f}  expected{3: 4.10f} availale{4: 4.10f}"'.format(
                    for_side, diff_val, trading_merit, expected_value, float(trading_row['available'])))
            if trading_merit > 0.0 and (float(trading_row['available']) * aveilable_reserve) > now_quantity:
                print( '!=^=^=^=^==============trading==={0}={1}================================='.format(for_side,cur_currency))
                print( '!=^= instrument: {0} quantity : {1: 4.10f} aveilable : {2} recently trade : {3: 4.10f} ==='.format(
                    now_instrument,trade_price,trading_row['available'],data_row[1]
                ))
                print('!=^= min   : "{0: 4.10f}"  max  : "{1: 4.10f}"  trading merit {2: 4.10f} expected{3: 4.10f} ==='.format(
                    res_row[1], res_row[2], trading_price, expected_value))
                print ("!------------> timestamp {0:%Y-%m-%d %H:%M:%S}".format(res_row[6]))
                print( '!=^=^=^=^===========================================================')
