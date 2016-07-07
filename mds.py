#!/usr/bin/env python


import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from sys import argv
import pandas as pd
from sklearn import manifold
from sklearn.metrics import euclidean_distances
import seaborn as sns
import scipy.spatial.distance as spd
from scipy.spatial.distance import squareform
import math
from sklearn.decomposition import PCA


try:
    argv[1]
    argv[2]
    argv[3]
    argv[4]
except:
    print 'Usage:'
    print '    python nmds.py <input_filename> <dissimilarity_measure> <skip_rows> <output_filename>'
    exit(1)

to_skip = [int(i) for i in argv[3].split(',')] if argv[3] else None
#print "to_skip:", to_skip

# load data
df = pd.read_table(argv[1], header=0, skiprows=to_skip, index_col=0)
#df = pd.read_table(argv[1], header=0, index_col=0) # test.txt
#print df

df = df.transpose()
#print df

df = df.as_matrix() # convert pandas.DataFrame to numpy.ndarray
#print df

# center the data
#print df.mean()
df -= df.mean()

output_filename = argv[4]+'_'

# compute distances
if argv[2] in 'euclidean':
    output_filename += 'euclidean'
    similarities = euclidean_distances(df)
elif argv[2] in 'braycurtis':
    output_filename += 'braycurtis'
    similarities = squareform(spd.pdist(df, "braycurtis"), checks=True)
elif argv[2] in 'lbraycurtis':
    output_filename += 'lbraycurtis'
    ranked = np.matrix([[(math.log(1.0+l) if l > 0.0 else 0.0) for l in np.nditer(d)] for d in df])
    #print ranked
    similarities = squareform(spd.pdist(ranked, "braycurtis"), checks=True)
elif argv[2] in 'sbraycurtis':
    output_filename += 'sbraycurtis'
    ranked = np.matrix([[(math.sqrt(l) if l > 0.0 else 0.0) for l in np.nditer(d)] for d in df])
    # print ranked
    similarities = squareform(spd.pdist(ranked, "braycurtis"), checks=True)

# print similarities

# metadata metaphlan mds
y = np.array([0, 0, 0, 0, 0, 0, 0, 0, # fei
              1, 1, 1, 1, 1, 1, 1, 1, # fem
              2, 2, 2, 2, 2, 2, 2]) # mim

# metadata humann mds
#y = np.array([2, 0, 0, 2, 2, 1, 1, 2,
#              1, 1, 2, 2, 1, 1, 0, 0,
#              0, 0, 2, 1, 0, 0, 1])

# # test.txt
# y = np.array([0, 0, # moms
#               1, 1, # chil
#               2, 2]) # dads

# MDS
mds = manifold.MDS(dissimilarity='precomputed')
pos = mds.fit(similarities).embedding_

# NMDS
# nmds = manifold.MDS(dissimilarity='precomputed', max_iter=1, metric=False)
# npos = nmds.fit_transform(similarities)

# rescale the data
pos *= np.sqrt((df**2).sum()) / np.sqrt((pos**2).sum())
# npos *= np.sqrt((df**2).sum()) / np.sqrt((npos**2).sum())

# rotate the data
clf = PCA(n_components=2)
pos = clf.fit_transform(pos)
# npos = clf.fit_transform(npos)

# draw MDS
fig = plt.figure()

for col, lbl, idx in zip(['g', 'r', 'b', 'y'], ['FEI', 'FEM', 'MIM', 'CST'], [0, 1, 2, 3]):
# for col, lbl, idx in zip(['r', 'g', 'b'], ['mom', 'chil', 'dad'], [0, 1, 2]):  # test.txt
    plt.scatter(pos[y == idx, 0], pos[y == idx, 1], c=col, label=lbl, s=[150]*len(y), alpha=0.89)

plt.legend()

print "output file:", output_filename+'_mds.pdf'
fig.savefig(output_filename+'_mds.pdf')

# # draw NMDS
# fig = plt.figure()

# for col, lbl, idx in zip(['g', 'r', 'b'], ['fei', 'fem', 'mim'], [0, 1, 2]):
# # for col, lbl, idx in zip(['r', 'g', 'b'], ['mom', 'chil', 'dad'], [0, 1, 2]):  # test.txt
#     plt.scatter(npos[y == idx, 0], npos[y == idx, 1], c=col, label=lbl)

# plt.legend()
# plt.title('NMDS')

# fig.savefig('nmds_'+output_filename+'.svg')
# fig.savefig('nmds_'+output_filename+'.png', dpi=300)
