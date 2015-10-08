#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.lda import LDA
from sys import argv
import pandas as pd
import numpy as np
import seaborn as sns


# load data
df = pd.read_table(argv[1], header=0, skiprows=[1, 2, 3, 4], index_col=0)
df = df / df.max()
df = df.dropna(axis=1, how='all') # drop all the columns (axis=1) which all values are NaN (happen when the column contains all zeros)
df = df.pow(2)
p = np.percentile(df, 95)
df[df > p] = p
df = df / df.max()

# load metadata
# md = pd.read_table(argv[2], header=0, index_col=0).transpose()
# md dataframe con pos e names come cols
# DA IMPLEMENTARE

# PCA
X = df.values[:,1:]
pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)

# Percentage of variance explained for each components
print('explained variance ratio (first two components): %s' % str(pca.explained_variance_ratio_))

colors = None # build as many colors as manny metadata

fig = plt.figure()

# for i, md_lbl in zip(md.pos.values(), md.names):
#     plt.scatter(X_r[md.pos == i, 0], X_r[md.pos == i, 1], c=colors[i], label=md_lbl)

plt.scatter([x for x, _ in X_r], [y for _, y in X_r], c='r', label='pca')

plt.legend()
plt.title('PCA')

fig.savefig("temp/pca.png", dpi=300)
