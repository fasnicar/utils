#!/usr/bin/env python


import sys


summ = 0
ref_lst = 0.0
alt_lst = 0.0

with open(sys.argv[1]) as f:
    for row in f.readlines()[1:]:
        _, ref, alt, lenn = row.strip().split('\t')
        summ += int(lenn)
        ref_lst += float(ref)*float(lenn)
        alt_lst += float(alt)*float(lenn)

clean = sys.argv[1][:sys.argv[1].rfind('.')]
clean = clean[:clean.find('_')]

with open(sys.argv[1]+'.new', 'w') as f:
    f.write('\t'.join(["gen", "ref", "alt", "len"]) + '\n')
    f.write('\t'.join([clean, '{:.5f}'.format(ref_lst/summ), '{:.5f}'.format(alt_lst/summ), str(summ)]) + '\n')
