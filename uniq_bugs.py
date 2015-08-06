#!/usr/bin/env python


from sys import argv


try:
    tsv = str(argv[1])
    cols = [int(i) for i in argv[2].split(',')]
    rows = [int(i) for i in argv[3].split(',')]
    outf = str(argv[4])
except:
    print "py uniq_bugs.py <tsv-mp2-merge> <col1,col2,..> <row1,row2,..> <output-name>"
    print "py uniq_bugs.py all.txt 3,6 all.png"
    print "cols and rows indexes start from 1!"
    exit(1)

labels = []
bugs_list = []
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

                for c in cols:
                    if float(r.strip().split(sep)[c-1]) > 0:
                        bugs_list.append(bug)
                        break

        row_count += 1

with open(outf, 'w') as f:
    f.write(sep.join(['bugs'] + labels) + '\n')
    f.write('\n'.join(bugs_list) + '\n')
