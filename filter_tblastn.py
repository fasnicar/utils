#!/usr/bin/env python


import os
import sys
import utils
from time import time
from glob import iglob
from argparse import ArgumentParser
from scipy.cluster import hierarchy


__date__ = '15 Apr 2015'
__email__ = 'f.asnicar@unitn.it'
__author__ = 'Francesco Asnicar'
__version__ = '0.01'


def read_params():
    """
    Parse the input parameters, performing some validity check.
    Return the parsed arguments.
    """
    parser = ArgumentParser(description="filter_tblastn.py (ver. "+__version__+" of "+__date__+"). Author: "+__author__+
        " ("+__email__+")")

    parser.add_argument('b6o_folder', nargs='?', type=str, help="", metavar='B6O_FOLDER')
    parser.add_argument('-e', '--extension', default='.b6o', type=str, help="")
    parser.add_argument('-v', '--verbose', action='store_true', help="")

    # name or flags
    # action - The basic type of action to be taken when this argument is encountered at the command line.
    # nargs - The number of command-line arguments that should be consumed.
    # const - A constant value required by some action and nargs selections.
    # default - The value produced if the argument is absent from the command line.
    # type - The type to which the command-line argument should be converted.
    # choices - A container of the allowable values for the argument.
    # required - Whether or not the command-line option may be omitted (optionals only).
    # help - A brief description of what the argument does.
    # metavar - A name for the argument in usage messages.
    # dest

    args = parser.parse_args()

    # Additional checks for input params
    if not args.b6o_folder:
        args.b6o_folder = './'
        if args.verbose: utils.info('no b6o_folder provided, current directory will be used.')

    if not args.b6o_folder.endswith('/'):
        args.b6o_folder = args.b6o_folder+'/'
        if args.verbose: utils.info('added "/" to b6o_folder: "'+args.b6o_folder+'"')

    if not args.extension.startswith('.'):
        args.extension = '.'+args.extension
        if args.verbose: utils.info('added "." to extension: "'+args.extension+'"')


    return args


def main(args):
    """
    """
    if not os.path.isdir(args.b6o_folder):
        utils.error('directory not found: "'+str(args.b6o_folder)+'"')
        return utils.FOLDER_NOT_FOUND

    b6o_files = iglob(args.b6o_folder+'*'+args.extension)
    contigs = {}

    for f in b6o_files:
        key = f[f.rfind('/')+1:]

        with open(f) as hf:
            for r in hf:
                tmp_lst = r.strip().split()
                dic = {} if key not in contigs else contigs[key]

                tmp_tmp_lst = [tmp_lst[0]]
                tmp_tmp_lst.append(float(tmp_lst[2]))
                tmp_tmp_lst += [int(e) for e in tmp_lst[3:10]]
                tmp_tmp_lst.append(float(tmp_lst[10]))
                tmp_tmp_lst.append(float(tmp_lst[11]))

                if tmp_lst[1] in dic:
                    dic[tmp_lst[1]].append(tmp_tmp_lst)
                else:
                    dic[tmp_lst[1]] = [tmp_tmp_lst]

                contigs[key] = dic

    for f, cc in contigs.items():
        for c, d in cc.items():
            points = [[dd[7]] for dd in d]
            points += [[dd[8]] for dd in d]

            # cluster start and end points
            y = hierarchy.linkage(points)
            z = hierarchy.median(y)

            print len(points)
            print z[:20]
            break
        break

    return utils.SUCCESS


if __name__ == "__main__":
    t0 = time()
    args = read_params()
    status = main(args)
    if args.verbose: utils.info('total time: '+str(int(time()-t0))+'s')
    sys.exit(status)
