#!/usr/bin/python
#coding: utf-8
#estimate_price.py
# import関連
import datetime
import sys
import os
sys.path.append('/home/yama/public_html/altcoins/source/lib/')
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import hitbtc_db

import warnings
#warnings.filterwarnings('ignore') # 実行上問題ない注意は非表示にします

args = sys.argv

instrument_str = 'ETHBTC'
if  len(args) > 1 :
    instrument_str = args[1]
debug = 1

span_start = 0.1
span_end = 0

table_get_col = {"label":0,"time":1,"min":2,"close":5}
# 2はmin,3はmax,4はopen,5はclose
data_kind = 5
data_kind_open = 4
data_kind_close = 5
# %matplotlib inline
# 30分毎なので47で1日 0:00と24:00がおなじになるように
time_ago = 47 * int(30 * (span_start - span_end))
# 評価パラメータをいくつ用いるか？
num_param = 1
# 単位時間何個分次の値を予測するか？
pre_time = 1

# データの読み込みのためライブラリオープン
db_access = hitbtc_db.HITBTCDB()
# symbols,timestamp ,min,max,open,close,volume
candle_data = db_access.get_recent_period(
    instrument=instrument_str, span_end=span_end, span_start=span_start)
value_disp = np.zeros(len(candle_data))

plt.style.use('seaborn-darkgrid')
# for chandle in candle_data :
#     print(chandle)

targ_data = np.array(candle_data)
# 現在時間によって個数が違うので計算が合わなくなる？
time_ago = targ_data.shape[0]
time_disp = np.zeros(time_ago)
print("time_ago:{}".format(time_ago))
print("targ_data.shape:{}".format(targ_data.shape))
print("targ_data:{}".format(targ_data))
print("LENGTH {0: 08d}".format(len(targ_data)))
# Xの初期化
X = np.zeros((len(targ_data) - 1))

# 開始時間をとっておいてその差分とする
start_time = 0
# 時間データをXに入れる
for i in range(0, (time_ago - 1)):
    if i == 0 :
        # start_time = targ_data[i, table_get_col["time"]].timestamp()
        start_time = targ_data[i, table_get_col["time"]]
    # X[i] = (targ_data[i, table_get_col["time"]].timestamp() - start_time) / 100
    #  X[i] = targ_data[i, table_get_col["time"]].timestamp()
    X[i] = - (targ_data[i, table_get_col["time"]] -
              datetime.datetime(1970, 1, 1)).total_seconds()
    print("X:{0} label:".format(X[i],))


# 出力画像の作成
fig = plt.figure()

# 被説明変数となる Y = pre_time後の終値-当日終値 を作成します
Y = np.zeros(len(targ_data) - 1)
D = np.zeros(len(targ_data) - 1)
data_label_name = ''
# minデータをYに入れる
for i in range(0, (time_ago - 1)):
    D[i] = abs(targ_data[i, data_kind_open] - targ_data[i, data_kind_close]) * 50
    Y[i] = targ_data[i, data_kind]


# 上で作った画像にplot
# ax = fig.add_subplot(1, 1, 1)
# ax.plot(X, Y, linestyle='--', color='b', label='y = min')
# subplot(行の数, 列の数, 何番目に配置しているか)
plt.subplot(2,1,1)
plt.plot(X, Y, linestyle='solid', color='b', marker='.', label='y = close')
plt.subplot(2,1,2)
plt.plot(X, D, linestyle='solid', color='r', marker='.', label='d = (|open - close|)*50')


# 凡例の表示
plt.legend()

# プロット表示(設定の反映)
plt.show()
