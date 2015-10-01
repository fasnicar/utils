#!/usr/bin/env python


import matplotlib.pyplot as plt
# from sklearn import datasets
from sklearn.decomposition import PCA
from sys import argv
import pandas as pd
import numpy as np


# load data
with open(argv[1], 'r') as mp_file:
    df = pd.read_table(argv[1], header=0, index_col=0)
    df = df / df.max()
    df = df.pow(2)
    p = np.percentile(df, 95)
    df[df > p] = p
    df = df / df.max()

X = df.values[:,1:]
pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)

# Percentage of variance explained for each components
print('explained variance ratio (first two components): %s' % str(pca.explained_variance_ratio_))

plt.figure()
for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
    plt.scatter(X_r[y == i, 0], X_r[y == i, 1], c=c, label=target_name)
plt.legend()
plt.title('PCA of IRIS dataset')

plt.show()
