#!/usr/bin/env python


from sys import argv


try:
    tsv = str(argv[1])
    skip_rows = [int(i) for i in argv[2].split(',')]
    mums = [int(i) for i in argv[3].split(',')]
    babies = [int(i) for i in argv[4].split(',')]
    outf = str(argv[5])
except:
    print "py shared_bugs.py <tsv-mp2-merge> <1,2,..> <mum1,mum2,..> <baby1,baby2,..> <output-name>"
    print "py shared_bugs.py all.txt 1 3,6 all.png"
    print "    skip_rows index start from 1, do not include the header!"
    print "    mums and babies indexes start from 1 and represent the couples of mum-baby!"
    exit(1)

labels = []
bugs_list = {}
header = True
row_count = 1
sep = ',' if tsv.endswith('.csv') else '\t'

couples = [(m, b) for b, m in zip(mums, babies)]

with open(tsv) as f:
    for r in f:
        if row_count not in skip_rows:
            if header:
                header = False
                labels = r.strip().split(sep)
            else:
                bug = str(r.strip().split(sep)[0])
                bugs_list[bug] = [float(s) for s in r.strip().split(sep)[1:]]

        row_count += 1

sep = '\t' if outf.endswith('.tsv') else ','

with open(outf, 'w') as f:
    f.write(sep.join(['bugs'] + labels) + '\n')

    for bug, abus in bugs_list.iteritems():
        if len([abu for abu in abus if abu > 0]) == len(abus):
            f.write(sep.join([bug] + [str(abu) for abu in abus]) + '\n')
