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

## 全体をうまくプロットしたいが出来なかったのでコメント
#sns.pairplot(df, hue="target")

# import some data to play with
X = iris.data[:, [0, 2]]
y = iris.target

# graph common settings
h = .02  # step size in the mesh
x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# ##################################################### func
def decision_boundary(clf, X, y, ax, title):
    clf.fit(X, y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    ax.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired, shading='auto')

    # Plot also the training points
    ax.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap=plt.cm.Paired)

    # label
    ax.set_title(title)
    ax.set_xlabel('sepal length')
    ax.set_ylabel('petal length')
# #####################################################

fig, axes = plt.subplots(1, 4, figsize=(12, 3))

for ax, n_neighbors in zip(axes, [1, 3, 6, 10]):
    title = "%s neighbor(s)" % (n_neighbors)
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    decision_boundary(clf, X, y, ax, title)

# プロット表示(設定の反映)
plt.show()
