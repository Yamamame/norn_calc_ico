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

# データの読み込みのためライブラリオープン
db_access = hitbtc_db.HITBTCDB()
targ_data = db_access.get_recent_period()

plt.style.use('seaborn-darkgrid')
print('{}'.format(targ_data))
