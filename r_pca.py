#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sys import argv
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import numpy as np
from numpy import matrix
import pickle
import seaborn as sns
from scipy.spatial.distance import squareform


rstats = importr('stats')
rbase = importr('base')

with open(argv[1], 'rb') as f:
    Y = pickle.load(f)

matt = squareform(Y, checks=True)
print matt
mat = []

for r in matt:
    for e in r:
        mat.append(e)

R_mat = rbase.matrix(robjects.vectors.FloatVector(mat), nrow=len(matt), byrow=True)
PCA = rstats.cmdscale(R_mat, k=2)
m = matrix(PCA)
y = np.array([0, 0, 0, 0, 0, 0, 0, 0,
              1, 1, 1, 1, 1, 1, 1, 1,
              2, 2, 2, 2, 2, 2, 2])

fig = plt.figure()

for col, lbl, idx in zip(['r', 'g', 'b'], ['fei', 'fem', 'mim'], [0, 1, 2]):
    plt.scatter(m[y == idx, 0], m[y == idx, 1], c=col, label=lbl)

plt.legend()
plt.title('PCA (R version)')
fig.savefig("temp/r_pca_prova.png", dpi=300)
