#!/usr/bin/env python


from sys import argv


try:
    tsv = str(argv[1])
    md_rows = [int(i) for i in argv[2].split(',')]
    mums = [int(i) for i in argv[3].split(',')]
    babies = [int(i) for i in argv[4].split(',')]
    milks = [int(i) for i in argv[5].split(',')]
    outf = str(argv[6])
except:
    print "py shared_bugs.py <tsv-mp2-merge> <md1,md2,..> <mum1,mum2,..> <baby1,baby2,..> <milk1,milk2,..> <output-name>"
    print "py shared_bugs.py all.txt 2,3 4,5 6,7 all.png"
    print "    metadata rows index start from 1, do not include the header!"
    print "    mums and babies indexes start from 1 and represent the couples of mum-baby!"
    exit(1)

labels = []
bugs_list = {}
header = True
row_count = 1
sep = ',' if tsv.endswith('.csv') else '\t'

tuples = [(m, b, i) for m, b, i in zip(mums, babies, milks)]
#print tuples

with open(tsv) as f:
    for r in f:
        if header:
            header = False
            labels.append(r.strip().split(sep))

            #print labels
            #for m, c, i in tuples:
            #    print labels[0][m-1],
            #    print labels[0][c-1],
            #    print labels[0][i-1]
            #print
            #exit(1)

        elif row_count in md_rows:
            labels.append(r.strip().split(sep))
        else:
            bug = str(r.strip().split(sep)[0])
            bugs_list[bug] = [float(s) for s in r.strip().split(sep)[1:]]

        row_count += 1

# look for shared bugs
shared = {}

for b, bl in bugs_list.iteritems():
    for m, c, i in tuples:
        if bl[m-2] >= 0.1 and bl[c-2] >= 0.1:
            print b, labels[0][m-1], bl[m-2], labels[0][c-1], bl[c-2]

            if b not in shared:
                shared[b] = bl

sep = '\t' if outf.endswith('.tsv') else ','

with open(outf, 'w') as f:
    f.write('\n'.join([sep.join(r) for r in labels]) + '\n')

    for b, bl in shared.iteritems():
        f.write(sep.join([b] + [str(v) for v in bl]) + '\n')
