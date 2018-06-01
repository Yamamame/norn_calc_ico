#!/usr/bin/python
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

#%matplotlib inline
# 30分毎なので48で1日
time_ago  =48 * 30
# 評価パラメータをいくつ用いるか？
num_param = 1
# 単位時間何個分次の値を予測するか？
pre_time = 1

# データの読み込みのためライブラリオープン
db_access = hitbtc_db.HITBTCDB()
# symbols,timestamp ,min,max,open,close,volume
candle_data = db_access.get_recent_period()

plt.style.use('seaborn-darkgrid')
# for chandle in candle_data :
#     print(chandle)

targ_data = np.array(candle_data)
print("%s" % targ_data)
print("LENGTH {0: 08d}".format(len(targ_data)))
X = np.zeros((len(targ_data), time_ago * num_param))
# closeの値で計算する
for i in range(0, time_ago):
    X[i:len(targ_data),i] = targ_data[0:len(targ_data)-i,5]
print("%s" % X)

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

# sns.set_style('darkgrid')
# pg = sns.pairplot(df)
# pg.savefig('./seaborn_pairplot_default.png')
