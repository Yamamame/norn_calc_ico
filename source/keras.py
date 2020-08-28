#!python
# keras.py
# TensorFlow と tf.keras のインポート
import tensorflow as tf
from tensorflow import keras

# ヘルパーライブラリのインポート
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images,
                               test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# [データの観察]
# モデルの訓練を行う前に、データセットのフォーマットを見てみましょう。
# 下記のように、訓練用データセットには28×28ピクセルの画像が60, 000枚含まれています。
# 同様に、訓練用データセットには60,000個のラベルが含まれます。
# ラベルはそれぞれ、0から9までの間の整数です。
# テスト用データセットには10,000個のラベルが含まれます。
print(train_images.shape)
print(len(train_labels))
print(train_labels)
print(len(test_labels))

# データの前処理
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()

train_images = train_images / 255.0

test_images = test_images / 255.0

plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

# このネットワークの最初の層は、tf.keras.layers.Flatten です。
# この層は、画像を（28×28ピクセルの）2次元配列から、28×28＝784ピクセルの、1次元配列に変換します。
# この層が、画像の中に積まれているピクセルの行を取り崩し、横に並べると考えてください。
# この層には学習すべきパラメータはなく、ただデータのフォーマット変換を行うだけです。
# ピクセルが１次元化されたあと、ネットワークは2つの tf.keras.layers.Dense 層となります。
# これらの層は、密結合あるいは全結合されたニューロンの層となります。
# 最初の Dense 層には、128個のノード（あるはニューロン）があります。
# 最後の層でもある2番めの層は、10ノードのsoftmax層です。
# この層は、合計が1になる10個の確率の配列を返します。
# それぞれのノードは、今見ている画像が10個のクラスのひとつひとつに属する確率を出力します。
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# モデルのコンパイル
# モデルが訓練できるようになるには、いくつかの設定を追加する必要があります。それらの設定は、モデルのコンパイル(compile）時に追加されます。
#     損失関数（loss function） —
#         訓練中にモデルがどれくらい正確かを測定します。
#         この関数の値を最小化することにより、訓練中のモデルを正しい方向に向かわせようというわけです。
#     オプティマイザ（optimizer）—
#         モデルが見ているデータと、損失関数の値から、どのようにモデルを更新するかを決定します。
#     メトリクス（metrics） —
#         訓練とテストのステップを監視するのに使用します。
#         下記の例ではaccuracy （正解率）、つまり、画像が正しく分類された比率を使用しています。
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# モデルの訓練
# ニューラルネットワークの訓練には次のようなステップが必要です。

# モデルに訓練用データを投入します—この例では train_images と train_labels の２つの配列です。
# モデルは、画像とラベルの対応関係を学習します。
# モデルにテスト用データセットの予測（分類）を行わせます—
# この例では test_images 配列です。その後、予測結果と test_labels 配列を照合します。
# 訓練を開始するには、model.fit メソッドを呼び出します。
# モデルを訓練用データに "fit"（適合）させるという意味です。
model.fit(train_images, train_labels, epochs=5)

# 正解率の評価
# 次に、テスト用データセットに対するモデルの性能を比較します。
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)
