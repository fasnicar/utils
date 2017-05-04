#!/usr/bin/env python3


import glob


for dirr in glob.iglob('CA_*'):
    print(dirr)
    header = []
    snprates = []

    for snprate in glob.iglob(dirr+'/[B|G]*.snprate'):
        with open(snprate) as f:
            for row in f:
                if not header and row.startswith('gen'):
                    header = row.strip().split('\t')
                elif not row.startswith('gen'):
                    snprates.append(row.strip().split('\t'))

    with open(dirr+'.snprate', 'w') as f:
        f.write('#{}\n'.format(dirr))
        f.write('{}\n'.format('\t'.join(header)))
        f.write('{}\n'.format('\n'.join(['\t'.join(a) for a in snprates])))
