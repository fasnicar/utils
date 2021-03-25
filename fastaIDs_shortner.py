#!/usr/bin/env python


__author__ = 'Francesco Asnicar (f.asnicar@unitn.it)'
__version__ = '0.1'
__date__ = '23 November 2020'


import os
import bz2
import sys
import argparse as ap
from Bio import SeqIO
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def info(s, init_new_line=False, exit=False, exit_value=0):
    if init_new_line:
        sys.stdout.write('\n')

    sys.stdout.write('{}'.format(s))
    sys.stdout.flush()

    if exit:
        sys.exit(exit_value)


def error(s, init_new_line=False, exit=False, exit_value=1):
    if init_new_line:
        sys.stderr.write('\n')

    sys.stderr.write('[e] {}\n'.format(s))
    sys.stderr.flush()

    if exit:
        sys.exit(exit_value)


def read_params():
    p = ap.ArgumentParser(description="FastaID_shortener loads fasta file(s) and shorten the IDs using an increasing number.", 
                          formatter_class=ap.ArgumentDefaultsHelpFormatter)
    p.add_argument('-i', '--input_folder', type=str, default='.', help="The input folder containing the fasta files to be shortened")
    p.add_argument('-t', '--type', default=None, choices=['n', 'a'],
                   help=('Specify the type of fasta, where "n" stands for nucleotides and provides the ".fna" extension for the output '
                         'file and "a" for amino acids and provides the ".faa" extesion for the output file. If not specified the ".fa" '
                         'extension for the output file will be used'))
    p.add_argument('--overwrite', action='store_true', default=False, help="Overwrite output file(s) if present")
    p.add_argument('--verbose', action='store_true', default=False, help="Makes it verbose")
    p.add_argument('-v', '--version', action='version', version='FastaID_shortener version {} ({})'.format(__version__, __date__),
                   help="Prints the current version and exit")

    return p.parse_args()


def check_args(args, command_line_arguments, verbose=False):
    if not os.path.isdir(args.input_folder):
        error('"{}" is not a folder'.format(args.input_folder), exit=True)

    if verbose:
        info('Arguments: {}\n\n'.format(vars(args)))


def is_fasta(f):
    return any((i for i in SimpleFastaParser(bz2.open(f, 'rt') if f.endswith('.bz2') else open(f))))


def main():
    args = read_params()

    if args.verbose:
        info('FastaID_shortener version {} ({})\n'.format(__version__, __date__))
        info('Command line: {}\n'.format(' '.join(sys.argv)), init_new_line=True)

    check_args(args, sys.argv, verbose=args.verbose)

    for fasta_i in os.listdir(args.input_folder):
        fasta_o = fasta_i.replace('.fa', '').replace('.fna', '').replace('.fasta', '').replace('.bz2', '') + '_short.'
        fasta_o += 'fna' if args.type == 'n' else 'faa' if args.type == 'a' else 'fa'

        if os.path.isfile(fasta_o) and not args.overwrite:
            error('output file "{}" exists and --overwrite not specified, skipping'.format(fasta_o))
            continue

        if not is_fasta(fasta_i):
            if args.verbose:
                info('skipping "{}" as it is not a fasta file\n'.format(fasta_i))

            continue

        if args.verbose:
            info('Reading "{}" and writing shortned version to "{}"\n'.format(fasta_i, fasta_o))

        with open(fasta_o, 'w') as f:
            SeqIO.write(
                (SeqRecord(Seq(seq), id=str(c), description='') 
                           for c, (idd, seq) 
                           in enumerate(SimpleFastaParser(bz2.open(fasta_i, 'rt') if fasta_i.endswith('.bz2') else open(fasta_i)))), 
                f, "fasta")


if __name__ == '__main__':
    main()
