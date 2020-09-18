#!python
# hello-tf.py
from sklearn.neighbors import KNeighborsClassifier
import tensorflow as tf
import multiprocessing as mp
from sklearn.datasets import load_iris
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# 結果的にnearlest neighborのみ？
# ########################main 
iris = load_iris()

# # データの詳細確認
# print(iris.DESCR)

# データの形を確認
print("shape :{0}".format(iris.data.shape))
print("names :{0}".format(iris.target_names))

# pandasで行列に格納
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df.loc[df['target'] == 0, 'target'] = "setosa"
df.loc[df['target'] == 1, 'target'] = "versicolor"
df.loc[df['target'] == 2, 'target'] = "virginica"

# 出来たデータをざっくり眺める
print(df.describe())
print(df.info())
print(df.shape)
print(df[:1].shape)

## 全体をうまくプロットしたいが出来なかったのでコメント
#sns.pairplot(df, hue="target")

# # import some data to play with
# X = iris.data[:, [0, 2]]
# y = iris.target

# googleのチュートリアルを参考に書いてみる###
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# 出来たデータをざっくり眺める
print(x_train.shape)
print(x_train[:1].shape)
print(y_train.shape)
print(y_train[:1].shape)
print(y_train)

# 設計図作成
# 層を積み重ねてtf.keras.Sequentialモデルを構築します。
# 訓練のためにオプティマイザと損失関数を選びます。
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
])
predictions = model(x_train[:1]).numpy()
print(predictions)

# tf.nn.softmax 関数はクラスごとにこれらのロジットを "確率" に変換します。
# これが活性化関数？
y_ = tf.nn.softmax(predictions).numpy()
print(y_)

# 損失関数
# losses.SparseCategoricalCrossentropy 損失関数は、
# ロジットと True の インデックスに関するベクトルを入力にとり、
# それぞれの標本についてクラスごとに損失のスカラーを返します
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# 最初の損失関数
# -tf.log(1/10) ~= 2.3になるらしい
print(loss_fn(y_train[:1], predictions).numpy())

model.compile(optimizer='adamax',
              loss=loss_fn,
              metrics=['accuracy'])
# model.fitは損失を最小化する？
model.fit(x_train, y_train, epochs=5)

# Model.evaluate メソッドはモデルの性能を検査します。
# これには通常 "検証用データセット" または "テストデータセット" を用います。
print(model.evaluate(x_test,  y_test, verbose=2))

probability_model = tf.keras.Sequential([
    model,
    tf.keras.layers.Softmax()
])

print("test :{0}".format(x_test[:5]))
print(probability_model(x_test[:5]))
