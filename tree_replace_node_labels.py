#!/usr/bin/env python


import sys
import argparse as ap
from Bio import Phylo
import os
import sys
sys.setrecursionlimit(10000)

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
    p.add_argument('-m', required=True, type=str,
                   help="the mapping file that maps the current node labels to the label to be added")
    p.add_argument('-t', default='\t', type=str, help="the separator of the mapping file")
    p.add_argument('-l', required=True, type=int,
                   help="the colum in the mapping file containing the label to be added, 0-indexed")
    p.add_argument('-n', default=0, type=int,
                   help="the column in the mapping file containing the node label, 0-indexed")
    p.add_argument('-s', default='|', type=str,
                   help="the separator of the new string and the current node label")
    p.add_argument('-o', default=False, action='store_true', help="ovewrite output file if exists")
    p.add_argument('-w', default=False, action='store_true',
                   help="if specified the labels in the tree will be wiped and replaced by the new labels")
    p.add_argument('--prefix', default=False, action='store_true',
                   help="if specified the new labels will be prefixed to the current node labels")

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
    elif os.path.exists(args['outtree']) and not args['o']:
        print('Output file: "{}" exists, specify -o for overwriting'.format(args['outtree']))
        sys.exit(1)

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
                if args['w']:
                    clade.name = mapp[clade.name]
                else:
                    new_label = ''

                    if args['prefix']:
                        new_label = ''.join([mapp[clade.name], args['s'], clade.name])
                    else:
                        new_label = ''.join([clade.name, args['s'], mapp[clade.name]])

                    clade.name = new_label
            else:
                print('node id "{}" not found in the mapping file'.format(clade.name))
                continue

    # write output tree
    tree = Phylo.write(tree, args['outtree'], args['f'])
