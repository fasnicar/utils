#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from sys import argv
import pandas as pd
from sklearn import manifold
from sklearn.decomposition import PCA
from sklearn.metrics import euclidean_distances
import seaborn as sns

# load data
df = pd.read_table(argv[1], header=0, skiprows=[1, 2, 3, 4], index_col=0)
df = df.as_matrix() # convert pandas.DataFrame to numpy.ndarray

similarities = euclidean_distances(df)

########
# NMDS #
########
nmds = manifold.MDS(metric=False, n_init=1, max_iter=3000, eps=1e-12, dissimilarity='precomputed')
npos = nmds.fit_transform(similarities)

# rescale
npos *= np.sqrt((df ** 2).sum()) / np.sqrt((npos ** 2).sum())

# rotate
clf = PCA(n_components=2)
npos = clf.fit_transform(npos)

fig = plt.figure()

plt.scatter(npos[:, 0], npos[:, 1], c='r', label='nmds')

plt.legend()
plt.title('NMDS')

fig.savefig("temp/nmds.png", dpi=300)

# #######
# # MDS #
# #######
# mds = manifold.MDS(max_iter=3000, eps=1e-9, dissimilarity="precomputed")
# pos = mds.fit(similarities).embedding_

# # rescale
# pos *= np.sqrt((df ** 2).sum()) / np.sqrt((pos ** 2).sum())

# # rotate
# clf = PCA(n_components=2)
# pos = clf.fit_transform(pos)

# fig = plt.figure()

# plt.scatter(pos[:, 0], pos[:, 1], c='r', label='mds')

# plt.legend()
# plt.title('MDS')

# fig.savefig("temp/mds.png", dpi=300)
