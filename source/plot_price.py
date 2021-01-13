#!/usr/bin/python
#coding: utf-8
#estimate_price.py
# import関連
import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/lib/')
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import hitbtc_db

import warnings
#warnings.filterwarnings('ignore') # 実行上問題ない注意は非表示にします

args = sys.argv
loop_flg = 1
instrument_strs = ['ETHBTC', 'XMRBTC', 'XMRETH', ]
data_dir = os.environ['HOME'] + '/hitbtc/'

# dbの接続情報を取得
f = open(data_dir + '.my.cnf', 'r')
db_host = "localhost"
db_user = ""
db_pass = ""
db_name = "altcoins"
config = -1

for line in f.read().splitlines():
    if '[mysql]' in line:
        config = 0
    if config >= 0:
        # 改行コードが除去されないので除去を同時に行う
        strkeydict = line.split('=')
        if 'user' in strkeydict[0]:
            db_user = strkeydict[1]
        if 'password' in strkeydict[0]:
            db_pass = strkeydict[1]
        if 'host' in strkeydict[0]:
            db_host = strkeydict[1]

instrument_str = 'ETHBTC'
if  len(args) > 1 :
    instrument_str = args[1]
    loop_flg=0
debug = 1

span_start = 0.5
span_end = 0

table_get_col = {"label":0,"time":1,"min":2,"close":5} # 2はmin,3はmax,4はopen,5はclose
data_kind = 5
data_kind_open = 4
data_kind_close = 5 # %matplotlib inline
# 30分毎なので47で1日 0:00と24:00がおなじになるように
time_ago = 47 * int(30 * (span_start - span_end))
# 評価パラメータをいくつ用いるか？
num_param = 1
# 単位時間何個分次の値を予測するか？
pre_time = 1
# 差分の定数
DIFFERENCE = 0.05

# plotのためのカウンター
plot_count = 0

# グラフの描画先の準備
fig = plt.figure(figsize=(8.0, 5.0))

# 出力画像の作成
ax = fig.subplots(2, len(instrument_strs))
# データの読み込みのためライブラリオープン
db_access = hitbtc_db.HITBTCDB()
# if loop_flg == 1 :
for instrument_str in instrument_strs :
    ## ここからループの中身
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
        # X[i] = (targ_data[i, table_get_col["time"]] -
        #         datetime.datetime(2015, 1, 1)).total_seconds() / 60
        X[i] = (targ_data[i, table_get_col["time"]] - start_time).total_seconds() / 60 /60
        # print("X:{0} label:".format(X[i],))

    # 被説明変数となる Y = pre_time後の終値-当日終値 を作成します
    Y = np.zeros(len(targ_data) - 1)
    D = np.zeros(len(targ_data) - 1)
    data_label_name = ''
    # minデータをYに入れる
    for i in range(0, (time_ago - 1)):
        D[i] = abs(targ_data[i, data_kind_open] - targ_data[i, data_kind_close]) * 50
        Y[i] = targ_data[i, data_kind]
    
    # より大きな日付を保存する
    # 初期化は十分小さい値を適当に設定
    post_date = datetime.datetime(2006, 4, 3, 9, 0, 0)
    # 直前の取引の価格を設定
    # [0]instrument,[1]price,[2]quantity,[3]side,[4]exec_date
    pre_trades = db_access.pre_trade_value(instrument=instrument_str)
    E = np.zeros(len(targ_data) - 1)
    print("exexdate:{}".format(pre_trades))
    for pre_trade in pre_trades:
        if pre_trade[3] == 'buy' :
            # pre_tradeの価格をXの数だけ作る
            R = (X * 0) + pre_trade[1]
            ax[0, plot_count].plot(X, R, linestyle='solid', color='g',
                                   marker='.', label='buy = ' + pre_trade[4].strftime('%Y/%m/%d'))
            if pre_trade[4] > post_date:
                post_date = pre_trade[4]
                E = (X * 0) + (pre_trade[1] * (1 + DIFFERENCE))
        else :
            # pre_tradeの価格をXの数だけ作る
            H = (X * 0) + pre_trade[1]
            ax[0, plot_count].plot(X, H, linestyle='solid', color='r',
                                   marker='.', label='sell = ' + pre_trade[4].strftime('%Y/%m/%d'))
            if pre_trade[4] > post_date:
                post_date = pre_trade[4]
                E = (X * 0) + (pre_trade[1] * (1 - DIFFERENCE))
    # print("E:{}".format(E))
    ax[0, plot_count].plot(X, E, linestyle='dashdot', color='Y',
                           marker='.', label='est = ' + post_date.strftime('%Y/%m/%d'))


    # 上で作った画像にplot
    # ax = fig.add_subplot(1, 1, 1)
    # ax.plot(X, Y, linestyle='--', color='b', label='y = min')
    # subplot(行の数, 列の数, 何番目に配置しているか)
    ax[0,plot_count].plot(X, Y, linestyle='solid', color='b',
                        marker='.', label='y = close')

    # 凡例の表示
    ax[0, plot_count].legend()
    # titleをつける
    ax[0, plot_count].set(title=instrument_str)

    ax[1, plot_count].plot(X, D, linestyle='solid', color='r', marker='.', label='d = (|open - close|)*50')
    # 凡例の表示
    ax[1, plot_count].legend()
    plot_count += 1
    


# プロット表示(設定の反映)
plt.show()

# ファイルに保存
fig.savefig("graph.png")