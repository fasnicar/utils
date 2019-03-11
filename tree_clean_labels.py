#!/usr/bin/env python


import sys
import argparse as ap
from Bio import Phylo


def read_params(args):
    p = ap.ArgumentParser(formatter_class=ap.ArgumentDefaultsHelpFormatter,
                          description='Remove offending chars from tree node labels')

    p.add_argument('intree', nargs='?', default=None, type=str,
                   help="the input tree, stdin if not present")
    p.add_argument('outtree', nargs='?', default=None, type=str,
                   help="the out file, stdout if not present")
    p.add_argument('-f', default='newick', type=str,
                   choices=['newick', 'nexus', 'nexml', 'phyloxml', 'cdao'],
                   help="in/out -put format")
    p.add_argument('-o', default='.|', type=str, help="the offending chars to be replace")
    p.add_argument('-r', default='_', type=str, help="the replace char")

    args = vars(p.parse_args())

    if not (len(args['o']) > 0):
        print('offending chars empty')
        sys.exit(1)

    if not (len(args['r']) > 0):
        print('replacing char empty')
        sys.exit(1)

    if not args['intree']:
        args['intree'] = sys.stdin

    if not args['outtree']:
        args['outtree'] = sys.stdout

    return args


def clean_lables(label, offendings, replace):
    for o in offendings:
        label = label.replace(o, replace)

    return label


if __name__ == "__main__":
    args = read_params(sys.argv)
    tree = Phylo.read(args['intree'], args['f'])

    for clade in tree.find_clades():
        if clade.name:
            clade.name = clean_lables(clade.name, args['o'], args['r'])

    tree = Phylo.write(tree, args['outtree'], args['f'])
