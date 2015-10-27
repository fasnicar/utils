#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sys import argv
import pandas as pd
import numpy as np
import seaborn as sns


# load data
df = pd.read_table(argv[1], header=0, skiprows=[1, 2, 3, 4], index_col=0)
df = df.transpose()
df = df / df.max()
df = df.dropna(axis=1, how='all') # drop all the columns (axis=1) which all values are NaN (happen when the column contains all zeros)
df = df.pow(2)
p = np.percentile(df, 95)
df[df > p] = p
df = df / df.max()

# load metadata
# md = pd.read_table(argv[2], header=None, index_col=0)
# md dataframe con pos e names come cols
# DA IMPLEMENTARE
y = np.array([0, 0, 0, 0, 0, 0, 0, 0,
              1, 1, 1, 1, 1, 1, 1, 1,
              2, 2, 2, 2, 2, 2, 2])

# PCA
X = df.values[:, 1:]
pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)

# print X_r

# Percentage of variance explained for each components
print('explained variance ratio (first two components): %s' % str(pca.explained_variance_ratio_))

colors = ['r', 'g', 'b'] # build as many colors as many metadata

fig = plt.figure()

for col, lbl, idx in zip(['r', 'g', 'b'], ['fei', 'fem', 'mim'], [0, 1, 2]):
    plt.scatter(X_r[y == idx, 0], X_r[y == idx, 1], c=col, label=lbl)

# plt.scatter([x for x, _ in X_r], [y for _, y in X_r], c='r', label='pca')

plt.legend()
plt.title('PCA')

fig.savefig("temp/pca_2.png", dpi=300)
