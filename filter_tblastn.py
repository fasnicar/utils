#!/usr/bin/env python


import os
import sys

import utils
import hashlib
from time import time
from glob import iglob
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from argparse import ArgumentParser
from bz2 import BZ2File
# from scipy.cluster import hierarchy
# import matplotlib
# matplotlib.use('PS')
# import matplotlib.pyplot as plt


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
    parser.add_argument('-i', '--input', type=str, required=True, help="")
    parser.add_argument('-o', '--output', default='tmp/', type=str, help="")
    parser.add_argument('-v', '--verbose', action='store_true', help="")
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

    if not args.input.endswith('/'):
        args.input += '/'
        if args.verbose: utils.info('added "/" to input folder: "'+args.input+'"')

    if not args.output.endswith('/'):
        args.output += '/'
        if args.verbose: utils.info('added "/" to output folder: "'+args.output+'"')

    return args


def notinclusters((xx, yy), clusters):
    """
    """
    reverse = True if xx > yy else False

    for x, y in clusters:
        if reverse and (x > y):
            if ((x <= xx) and (xx <= y)) and ((x <= yy) and (yy <= y)):
                return False
        elif not reverse and (x < y):
            if ((y <= xx) and (xx <= x)) and ((y <= yy) and (yy <= x)):
                return False

    return True


def longest_not_overlapping(points):
    """
    """
    spoints = sorted(points, key=lambda x: abs(x[1]-x[0]), reverse=True)
    lno = [spoints[0]]

    for a, b in spoints[1:]:
        to_add = True

        for x, y in lno:
            if not (((a < x) and (b < x) and (a < y) and (b < y)) or
                    ((a > x) and (b > x) and (a > y) and (b > y))):
                to_add = False

        if to_add: lno.append((a, b))

    return lno


def find_clusters(reprs, points, f1, f2, reverse=True):
    """
    """
    clusters = set()

    for x, y in reprs:
        xyrev = False
        if x > y: xyrev = True
        tmp_clusters = set()

        if (not reverse) and (not xyrev):
            for a, b in points:
                if ((x != a) and (y != b)) and notinclusters((a, b), tmp_clusters):
                    if ((a >= x) and (a <= y)) and ((b >= x) and (b <= y)) or \
                       ((a <= x)) and ((b >= x) and (b <= y)) or \
                       ((a >= x) and (a <= y)) and ((b >= y)):
                        tmp_clusters |= set([(f1(x, a), f2(y, b))])
        elif reverse and xyrev:
            for a, b in points:
                if ((x != a) and (y != b)) and notinclusters((a, b), tmp_clusters):
                    if ((a >= x) and (a <= y)) and ((b >= x) and (b <= y)) or \
                       ((a <= x)) and ((b >= x) and (b <= y)) or \
                       ((a >= x) and (a <= y)) and ((b >= y)):
                        tmp_clusters |= set([(f1(x, a), f2(y, b))])

        if not tmp_clusters: tmp_clusters |= set([(x, y)])
        clusters |= set([(f1([a for a, _ in tmp_clusters]), f2([b for _, b in tmp_clusters]))])

    return clusters


def main(args):
    """
    """
    if not os.path.isdir(args.b6o_folder):
        utils.error('directory not found: "'+str(args.b6o_folder)+'"')
        return utils.FOLDER_NOT_FOUND

    if not os.path.isdir(args.input):
        os.mkdir(args.input)
        utils.error('directory not found: "'+str(args.input)+'"')
        exit(utils.FOLDER_NOT_FOUND)

    if not os.path.isdir(args.output):
        os.mkdir(args.output)
        utils.info('directory created: "'+str(args.output)+'"')

    b6o_files = iglob(args.b6o_folder+'*'+args.extension)
    contigs = {}

    if args.verbose: utils.info('reading tblastn files')

    for f in b6o_files:
        key = f[f.rfind('/')+1:f.rfind('.')]

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

    if args.verbose: utils.info('clustering')

    for f, cc in contigs.items():
        clusters = {}

        for c, d in cc.items():
            clusters[c] = set()
            yerev = []
            norev = []

            for dd in d:
                if dd[7] > dd[8]:
                    yerev.append((dd[7], dd[8]))
                else:
                    norev.append((dd[7], dd[8]))

            if norev:
                lno = longest_not_overlapping(norev) # find longest and not-overlapping segments
                clusters[c] |= find_clusters(lno, norev, min, max, reverse=False) # search for clusters

            if yerev:
                lno = longest_not_overlapping(yerev) # find longest and not-overlapping segments
                clusters[c] |= find_clusters(lno, yerev, max, min, reverse=True) # search for clusters

        # open input file and extract and translate the clusters
        proteome = []
        ff = None

        if os.path.isfile(args.input+f+'.fna'):
            ff = open(args.input+f+'.fna')
            if args.verbose: utils.info('reading input file: '+args.input+f+'.fna')
        elif os.path.isfile(args.input+f+'.fna.bz2'):
            ff = BZ2File(args.input+f+'.fna.bz2')
            if args.verbose: utils.info('file opened: '+args.input+f+'.fna.bz2')
        else:
            utils.info('file not found: '+args.input+f+'.fna(.bz2)')

        if ff:
            for record in SeqIO.parse(ff, 'fasta'):
                for contig, cpoints in clusters.items():
                    if record.id in contig:
                        for s, e in cpoints:
                            reverse = False

                            if s > e:
                                s, e = e, s
                                reverse = True

                            sequence = Seq(str(record.seq)[s-1:e])

                            while (len(sequence) % 3) != 0: # if sequence no div by 3, add Ns
                                sequence += Seq('N')

                            if reverse: sequence = sequence.reverse_complement()
                            rev = ':c' if reverse else ':' # reverse or not
                            seqid = f+'_'+record.id+rev+str(s)+'-'+str(e)
                            aminoacids = Seq.translate(sequence)
                            proteome.append(SeqRecord(aminoacids, id=seqid, description=''))

            ff.close()

            # make sure that the output file does not exists
            if os.path.isfile(args.output+f+'.faa'):
                fold = str(f)
                hash = hashlib.sha1()
                hash.update(str(time()))
                f += str(hash.hexdigest()[:4])
                utils.info('file already exists: '+fold+', written output file: '+f)

            # write output file
            with open(args.output+f+'.faa', 'w') as ff:
                SeqIO.write(proteome, ff, 'fasta')
                if args.verbose: utils.info('written output file: '+args.output+f+'.faa')

    return utils.SUCCESS


if __name__ == "__main__":
    t0 = time()
    args = read_params()
    status = main(args)
    if args.verbose: utils.info('total time: '+str(int(time()-t0))+'s')
    sys.exit(status)
