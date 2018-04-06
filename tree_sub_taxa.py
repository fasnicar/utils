#!/usr/bin/env python


import sys
import argparse as ap
from Bio import Phylo
import os


def read_params(args):
    p = ap.ArgumentParser(description='Append a label in front of the current node labels')

    p.add_argument('intree', nargs='?', default=None, type=str,
                   help="the input tree, stdin if not present")
    p.add_argument('outtree', nargs='?', default=None, type=str,
                   help="the out file, stdout if not present")
    p.add_argument('-f', default='newick', type=str,
                   choices=['newick', 'nexus', 'nexml', 'phyloxml', 'cdao'],
                   help="inp/out -put format, default = newick")
    p.add_argument('-m', required=True, type=str,
                   help="the mapping file that maps the current node labels to the label to be appended")
    p.add_argument('-t', default='\t', type=str, help="the separator of the mapping file, default = TAB")
    p.add_argument('-l', required=True, type=int,
                   help="the colum in the mapping file containing the label to be appended")
    p.add_argument('-n', default=0, type=int,
                   help="the column in the mapping file containing the node label, default = 0 (first column)")
    p.add_argument('-s', default='|', type=str,
                   help="the separator of the new string and the current node label, default = |")

    args = vars(p.parse_args())

    if not os.path.isfile(args['m']):
        print('mapping file "{}" is not a valid a file'.format(args['m']))
        sys.exit(1)

    if len(args['t']) > 1:
        print('separator must be one character')
        sys.exit(1)

    if not args['intree']:
        args['intree'] = sys.stdin

    if not args['outtree']:
        args['outtree'] = sys.stdout

    return args


if __name__ == "__main__":
    args = read_params(sys.argv)
    tree = Phylo.read(args['intree'], args['f'])
    mapp = {}

    # read mapping file
    with open(args['m']) as f:
        for row in f:
            node_id = row.strip().split(args['t'])[args['n']]
            label = row.strip().split(args['t'])[args['l']]

            if node_id not in mapp:
                mapp[node_id] = label
            else:
                print('node id "{}" duplicated'.format(node_id))
                sys.exit(1)

    # renaming node labels
    for clade in tree.find_clades():
        if clade.name:
            if clade.name in mapp:
                clade.name = ''.join([mapp[clade.name], args['s'], clade.name])
            else:
                print('node id "{}" not found in the mapping file'.format(clade.name))
                continue

    # write output tree
    tree = Phylo.write(tree, args['outtree'], args['f'])
