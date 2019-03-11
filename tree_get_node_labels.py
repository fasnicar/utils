#!/usr/bin/env python


import sys
import argparse as ap
from Bio import Phylo


def read_params(args):
    p = ap.ArgumentParser(formatter_class=ap.ArgumentDefaultsHelpFormatter,
                          description='Print to stdout the tree node labels')

    p.add_argument('intree', nargs='?', default=None, type=str,
                   help="the input tree, stdin if not present")
    p.add_argument('-f', default='newick', type=str,
                   choices=['newick', 'nexus', 'nexml', 'phyloxml', 'cdao'],
                   help="input format")

    args = vars(p.parse_args())

    if not args['intree']:
        args['intree'] = sys.stdin

    return args


if __name__ == "__main__":
    args = read_params(sys.argv)
    tree = Phylo.read(args['intree'], args['f'])

    for clade in tree.find_clades():
        if clade.name:
            sys.stdout.write(clade.name + '\n')
