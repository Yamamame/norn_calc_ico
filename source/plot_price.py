#!/usr/bin/python3
#coding: utf-8
#estimate_price.py
# import関連
import sys
sys.path.append('/home/yama/public_html/py_practice/lib/')
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import hitbtc_db

import warnings
#warnings.filterwarnings('ignore') # 実行上問題ない注意は非表示にします

debug = 1

span_start = 0.25
span_end = 0
# 2はmin,3はmax,4はopen,5はclose
data_kind = 5
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
candle_data = db_access.get_recent_period(span_end=span_end, span_start=span_start)
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
print("LENGTH {0: 08d}".format(len(targ_data)))
# Xの初期化
X = np.zeros((len(targ_data), time_ago * num_param))
print("X:{}".format(X))

# closeの値で計算する
for i in range(0, (time_ago - 1)):
    # print("{}".format(targ_data[i, 1]))
    X[i:len(targ_data), i] = targ_data[0:len(targ_data)-i, data_kind]
    
print("targ_data.shape:{0}".format(targ_data.shape))
print("time_ago:{0}".format(time_ago))
print("xdim:{0}".format(X.ndim))
# print("{}".format(X))


for i in range(0, time_ago):
    # print("{0}".format(i))
    time_disp[i] = targ_data[i, 1].timestamp()
    value_disp[i] = (targ_data[i, 2] + targ_data[i, 3]) /2
# print("%s" % time_disp)
print("X.shape    :{0}".format(X.shape))
print("value.shape:{0}".format(value_disp.shape))
print("X:{}".format(X))

# 被説明変数となる Y = pre_time後の終値-当日終値 を作成します
Y = np.zeros(len(targ_data))

Y[0:len(Y)-pre_time] = X[pre_time:len(X),0] - X[0:len(X)-pre_time,0]

original_X = np.copy(X) # コピーするときは、そのままイコールではダメ
tmp_mean = np.zeros(len(X))

for i in range(time_ago,len(X)):
    tmp_mean[i] = np.mean(original_X[i-time_ago+1:i+1,0]) # 25日分の平均値
    for j in range(0, X.shape[1]):
        X[i,j] = (X[i,j] - tmp_mean[i]) # Xを正規化
    Y[i] =  Y[i]  # X同士の引き算しているので、Yはそのまま

print("time_disp.s:{0}".format(time_disp.shape))
print("value_disp.s:{0}".format(value_disp.shape))
print("X:{}".format(X))
print("Y:{}".format(Y))
# 出力画像の作成
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(time_disp, value_disp, linestyle='--', color='b', label='y = sin(x)')
# ax.plot(X[:,1], Y, linestyle='--', color='b', label='y = sin(x)')
# 凡例の表示
plt.legend()

# プロット表示(設定の反映)
plt.show()
