#!/usr/bin/env python


from sys import argv


header = None
cleaned_data = {}

with open(argv[1]) as f:
    for row in f:
        if not header:
            header = row.strip().split('\t')
        else:
            gf = row.strip().split('\t')[0]
            data = [int(a) for a in row.strip().split('\t')[1:]]

            if (sum(data) != 1) and (sum(data) != len(header)-2):
                cleaned_data[gf] = data

with open(argv[1][:argv[1].rfind('.')]+'_clean.csv', 'w') as f:
    f.write('\t'.join(['']+header) + '\n')
    f.write('\n'.join(['\t'.join([k]+[str(a) for a in v]) for k,v in cleaned_data.iteritems()]) + '\n')
