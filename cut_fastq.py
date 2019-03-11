#!/usr/bin/env python


import sys
import os
from glob import glob
import bz2
from Bio import SeqIO


d = sys.argv[1]
print(d)

if not os.path.isdir(os.path.join('/shares/CIBIO-Storage/CM/scratch/data/meta/Japan_CRC/reads_90', d)):
    os.mkdir(os.path.join('/shares/CIBIO-Storage/CM/scratch/data/meta/Japan_CRC/reads_90', d))

for f in glob(os.path.join('/shares/CIBIO-Storage/CM/scratch/data/meta/Japan_CRC/reads', d, '*R*.fastq.bz2')):
    print(f)

    with bz2.open(os.path.join('/shares/CIBIO-Storage/CM/scratch/data/meta/Japan_CRC/reads_90', d, os.path.basename(f)), 'wt') as o:
        for r in SeqIO.parse(bz2.open(f, 'rt'), 'fastq'):
            o.write(r[:90].format('fastq'))
