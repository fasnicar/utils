#!/usr/bin/env python


import os
import sys
import utils
from time import time
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from argparse import ArgumentParser


__date__ = '26 Mar 2015'
__email__ = 'f.asnicar@unitn.it'
__author__ = 'Francesco Asnicar'
__version__ = '0.01'


def read_params():
    """
    Parse the input parameters, performing some validity check.
    Return the parsed arguments.
    """
    parser = ArgumentParser(description="aln_stats.py (ver. "+__version__+" of "+__date__+"). Author: "+__author__+" ("
        +__email__+")")

    parser.add_argument('total_alignment', nargs='?', type=str, help="The total (final) alignment file produced by "
        "PhyloPhlan. A thorough set of statical data will be provided.", metavar='TOTALN')

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

    return args


def main(args):
    """
    """
    if not args.total_alignment:
        utils.error('invalid argument: "'+str(args.total_alignment)+'"')
        return utils.INVALID_ARGS

    if not os.path.isfile(args.total_alignment):
        utils.error('file not found: "'+str(args.total_alignment)+'"')
        return utils.FILE_NOT_FOUND

    with open(args.total_alignment, 'rU') as f:
        alignments = SeqIO.parse(f, "fasta")
        i = 0

        for alignment in alignments:
            i += 1
            len_aln = len(alignment.seq)
            gaps = alignment.seq.count('-')
            print alignment.id, "len:", len_aln, "gaps:", gaps, "aln:", len_aln-gaps

        print "total alignments:", i

    return utils.SUCCESS


if __name__ == "__main__":
    t0 = time()
    args = read_params()
    status = main(args)
    utils.info("total time: "+str(int(time()-t0))+"s")
    sys.exit(status)
