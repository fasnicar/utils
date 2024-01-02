#!/usr/bin/env python


import sys
import argparse as ap
import os
import sys
import dendropy


def read_params(args):
    p = ap.ArgumentParser(formatter_class=ap.ArgumentDefaultsHelpFormatter,
                          description='Add a label in front of the current node labels')

    p.add_argument('intree', nargs='?', default=None, type=str,
                   help="the input tree, stdin if not present")
    p.add_argument('outtree', nargs='?', default=None, type=str,
                   help="the out file, stdout if not present")
    p.add_argument('-f', default='newick', type=str,
                   choices=['newick', 'nexus', 'nexml', 'phyloxml', 'cdao'],
                   help="inp/out -put format")
    p.add_argument('-r', required=True, type=str, help="the file with the node labels to remove")
    p.add_argument('-o', default=False, action='store_true', help="ovewrite output file if exists")

    args = vars(p.parse_args())

    if not os.path.isfile(args['r']):
        print('node labels file "{}" is not a valid a file'.format(args['m']))
        sys.exit(1)

    if not args['intree']:
        args['intree'] = sys.stdin

    if not args['outtree']:
        args['outtree'] = sys.stdout
    elif os.path.exists(args['outtree']) and not args['o']:
        print('Output file: "{}" exists, specify -o for overwriting'.format(args['outtree']))
        sys.exit(1)

    return args


def remove_leaves(tree, leaves_to_remove):
    for leaf_label in leaves_to_remove:
        leaf_node = tree.find_node_with_taxon_label(leaf_label)
        if leaf_node:
            tree.prune_subtree(leaf_node)


if __name__ == "__main__":
    args = read_params(sys.argv)

    leaves_to_remove = [i.strip() for i in open(args['r'])]
    tree = dendropy.Tree.get(data=open(args['intree']).readlines()[0], schema="newick")
    remove_leaves(tree, leaves_to_remove)
    tree.write_to_path(args['outtree'], schema='newick')
