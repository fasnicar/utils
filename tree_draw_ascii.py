#!/usr/bin/env python


import sys
import argparse as ap
from Bio import Phylo


def read_params(args):
    p = ap.ArgumentParser(description='Remove offending chars from tree node labels')

    p.add_argument('intree', nargs='?', default=None, type=str,
                   help="the input tree, stdin if not present")
    p.add_argument('-f', default='newick', type=str,
                   choices=['newick', 'nexus', 'nexml', 'phyloxml', 'cdao'],
                   help="inp/out -put format")

    args = vars(p.parse_args())

    if not args['intree']:
        args['intree'] = sys.stdin

    return args


if __name__ == "__main__":
    args = read_params(sys.argv)
    tree = Phylo.read(args['intree'], args['f'])
    Phylo.draw_ascii(tree)
