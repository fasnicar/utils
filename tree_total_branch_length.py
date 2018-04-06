#!/usr/bin/env python


import sys
import argparse as ap
from Bio import Phylo


def read_params(args):
    p = ap.ArgumentParser(description='Compute the total branch length of the provided tree')

    p.add_argument('intree', default=None, type=str,
                   help="the input tree, stdin if not present")
    p.add_argument('-f', default='newick', type=str,
                   choices=['newick', 'nexus', 'nexml', 'phyloxml', 'cdao'],
                   help="input format")

    args = vars(p.parse_args())

    if not args['intree']:
        args['intree'] = sys.stdin

    return args


def clean_lables(label, offendings, replace):
    for o in offendings:
        label = label.replace(o, replace)

    return label


if __name__ == "__main__":
    args = read_params(sys.argv)
    tree = Phylo.read(args['intree'], args['f'])
    print(tree.total_branch_length())
