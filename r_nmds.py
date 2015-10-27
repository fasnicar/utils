#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from sys import argv
from sklearn import manifold
from numpy import matrix
import pickle
import seaborn as sns
from scipy.spatial.distance import squareform


with open(argv[1], 'rb') as f:
    Y = pickle.load(f)

mat = squareform(Y, checks=True)

mds = manifold.MDS(dissimilarity="precomputed", n_components=2, n_jobs=1, random_state=3)
npos = matrix(mds.fit_transform(matrix(mat)))
# metadata
y = np.array([0, 0, 0, 0, 0, 0, 0, 0,
              1, 1, 1, 1, 1, 1, 1, 1,
              2, 2, 2, 2, 2, 2, 2])

fig = plt.figure()

for col, lbl, idx in zip(['r', 'g', 'b'], ['fei', 'fem', 'mim'], [0, 1, 2]):
    plt.scatter(npos[y == idx, 0], npos[y == idx, 1], c=col, label=lbl)

plt.legend()
plt.title('NMDS (R version)')

fig.savefig("temp/r_nmds.png", dpi=300)
