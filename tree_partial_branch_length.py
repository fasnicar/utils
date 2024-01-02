#!/usr/bin/env python


import sys
import argparse as ap
from Bio import Phylo
import os


def read_params(args):
    p = ap.ArgumentParser(formatter_class=ap.ArgumentDefaultsHelpFormatter,
                          description='Compute the partial branch length of a set of leaves')

    p.add_argument('intree', nargs='?', default=None, type=str,
                   help="the input tree, stdin if not present")
    p.add_argument('-f', default='newick', type=str,
                   choices=['newick', 'nexus', 'nexml', 'phyloxml', 'cdao'],
                   help="inp/out -put format")
    p.add_argument('-l', required=True, type=str,
                   help="the set of leaves (file or comma-separated values) to use for computing the partial branch length")

    args = vars(p.parse_args())

    if os.path.isfile(args['l']):
        args['l'] = [r.strip() for r in open(args['l']) if r.strip()]
    else:  # the input list is given as comma-separated values
        args['l'] = args['l'].split(',')

    if not args['intree']:
        args['intree'] = sys.stdin

    return args


def partial_branch_length(clade, selective_targets):

    def _partial_branch_length_(clade, selective_targets):
        if clade.is_terminal() and clade.name in selective_targets:
            return [clade.branch_length] if clade.branch_length else [0.0]

        if not any([c.name in selective_targets for c in clade.get_terminals()]):
            return [0.0]

        ret = [0.0]

        for c in clade.clades:
            ret += [partial_branch_length( c, selective_targets)]

        ret += [clade.branch_length] if clade.branch_length else [0.0]
        return ret

    return sum(_partial_branch_length_(clade,selective_targets))


if __name__ == "__main__":
    args = read_params(sys.argv)
    tree = Phylo.read(args['intree'], args['f'])

    print(partial_branch_length(tree.clade, args['l']))
