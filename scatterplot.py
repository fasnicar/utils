#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
from sys import argv
import matplotlib.pyplot as plt

try:
    tsv = str(argv[1])
    colX, colY = argv[2].split(',')
    outf = str(argv[3])
except:
    print "py scatterplot.py <tsv-mp2-merge> <colX>,<colY> <output-name>"
    print "py scatterplot.py all.txt 3,6 all.png"
    print "cols indexes start from 1!"
    exit(1)

colX = int(colX)
colY = int(colY)
x_values = []
y_values = []
x_label = ""
y_label = ""
header = True

with open(tsv) as f:
    for r in f:
        if header:
            x_label = str(r.strip().split()[colX-1])
            y_label = str(r.strip().split()[colY-1])
            header = False
        else:
            x_values.append(float(r.strip().split()[colX-1]))
            y_values.append(float(r.strip().split()[colY-1]))

print x_label, x_values
print y_label, y_values

fig, _ = plt.subplots(nrows=1, ncols=1) # create figure & 1 axis
plt.scatter(x_values, y_values, alpha=0.67)
fig.savefig(outf) # save the figure to file
plt.close(fig)
