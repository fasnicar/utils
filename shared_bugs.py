#!/usr/bin/env python


from sys import argv


try:
    tsv = str(argv[1])
    cols = [int(i) for i in argv[2].split(',')]
    rows = [int(i) for i in argv[3].split(',')]
    outf = str(argv[4])
except:
    print "py shared_bugs.py <tsv-mp2-merge> <col1,col2,..> <row1,row2,..> <output-name>"
    print "py shared_bugs.py all.txt 3,6 all.png"
    print "cols and rows indexes start from 1!"
    exit(1)

labels = []
bugs_list = {}
header = True
row_count = 1
sep = ',' if tsv.endswith('.csv') else '\t'

with open(tsv) as f:
    for r in f:
        if row_count not in rows:
            if header:
                header = False

                for c in cols:
                    labels.append(r.strip().split(sep)[c-1])
            else:
                bug = str(r.strip().split(sep)[0])
                bugs_list[bug] = []

                for c in cols:
                    bugs_list[bug].append(float(r.strip().split(sep)[c-1]))

        row_count += 1

sep = '\t' if outf.endswith('.tsv') else ','

with open(outf, 'w') as f:
    f.write(sep.join(['bugs'] + labels) + '\n')

    for bug, abus in bugs_list.iteritems():
        if len([abu for abu in abus if abu > 0]) == len(abus):
            f.write(sep.join([bug] + [str(abu) for abu in abus]) + '\n')
