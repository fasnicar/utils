#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sys import argv
import pandas as pd
from sklearn import manifold
from sklearn.decomposition import PCA
from sklearn.metrics import euclidean_distances
import seaborn as sns

# load data
df = pd.read_table(argv[1], header=0, skiprows=[1, 2, 3, 4], index_col=0)

similarities = similarities = euclidean_distances(df)

nmds = manifold.MDS(metric=False, n_init=1, max_iter=3000, eps=1e-12, dissimilarity='precomputed')
npos = nmds.fit_transform(similarities)

# Rotate the data
clf = PCA(n_components=2)
npos = clf.fit_transform(npos)

fig = plt.figure()

plt.scatter(npos[:, 0], npos[:, 1], c='r', label='nmds')

plt.legend()
plt.title('NMDS')

fig.savefig("temp/nmds.png", dpi=300)
