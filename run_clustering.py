#!/usr/bin/env python

import sys
import argparse as ap
import numpy as np
import itertools
import fastcluster
import scipy.cluster.hierarchy as hier

def read_params(args):
	parser = ap.ArgumentParser(description='Run clustering on genomes')
	arg = parser.add_argument
	arg( 'inp_f', metavar='INPUT_FILE', nargs='?', default=sys.stdin, type=str, help="the input distance file [stdin if not present]")
	arg( 'out_f', metavar='OUTPUT_FILE', nargs='?', default=None, type=str, help="the output file [stdout if not present]")
	arg( '-t','--threshold', default=0.05, type=float, help="threshold value")

	return vars(parser.parse_args())

if __name__ == "__main__":
	par = read_params(sys.argv)

	fid = open(par['inp_f'], 'r')
	ind = fid.readline().rstrip().split('\t')[1:]
	f = []
	c = 2
	for s in fid:
		f.append(s.rstrip().split('\t')[c:])
		c = c+1
	fid.close()
	f = list(itertools.chain(*f))
	
	z = fastcluster.linkage(f, method='average', preserve_input=False)
	l = hier.fcluster(z, par['threshold'], criterion='distance')

	if par['out_f']:
		fidout = open(par['out_f'],'w')
	else:
		fidout = sys.stdout

	for t in range(len(ind)):
		fidout.write(ind[t] + '\t' + str(l[t]) + '\n')

	if par['out_f']:
		fidout.close()
