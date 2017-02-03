#!/usr/bin/env python

import glob
import os
import sys
import subprocess
import argparse as ap
import pandas as pd
from Bio import SeqIO

def read_params(args):
        parser = ap.ArgumentParser(description='Compute coverage from bowtie2 output')
        arg = parser.add_argument
        arg('inp_f', metavar='INPUT_FILE', nargs='?', default=None, type=str, help="the input sorted bam file")
        arg( 'reference_path', metavar='REFERENCE_PATH', nargs='?', default=None, type=str, help="the path with reference genome files")
        arg( '-z','--reference_identifier', type=str, default='*.fna', help="the reference genome identifier")
        return vars(parser.parse_args())

if __name__ == '__main__':
        par = read_params(sys.argv)

        d = subprocess.check_output('bedtools genomecov -dz -ibam ' + par['inp_f'], shell=True)
        d = pd.DataFrame([s.split('\t') for s in d.split('\n')[:-1]])

        f_name = []
        f_id = []
        f_len = []
        for file in glob.glob(par['reference_path'] + par['reference_identifier']):
                f = []
                fid = open(file, "rU")
                for record in SeqIO.parse(fid,'fasta'):
                        f.append(record)
                fid.close()
                f_name.append(file)
                f_id.append([t.id for t in f])
                f_len.append([len(t) for t in f])

        f_count = []
        f_perc = []
        for t in range(len(f_name)):
                f_count.append(len(d.loc[d[0].isin(f_id[t])]))
                f_perc.append(float(f_count[t])/sum(f_len[t]))
        ind_sort = sorted(range(len(f_perc)),key=lambda x:f_perc[x])

        fid = open(par['inp_f'] + '.stats', 'w')
        for t in ind_sort:
                fid.write(f_name[t].split('/')[-1] + '\t' + str(sum(f_len[t])) + '\t' + str(f_count[t]) + '\t' + str(f_perc[t]) + '\n')
        fid.close()
