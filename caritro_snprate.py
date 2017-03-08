#!/usr/bin/env python3


import glob


files = glob.iglob('CA_*/*.indel.vcf')

for file in files:
    print(file)
    out_file = file[:file.find('.')]+'.snprate'
    data = {}

    with open(file) as f:
        for row in f:
            if not row.startswith('#'):
                rows = row.strip().split('\t')
                dp4_values = []

                for a in rows[7].split(';'):
                    if a.split('=')[0] == 'DP4':
                        dp4_values = [int(b) for b in a.split('=')[1].split(',')]

                if sum(dp4_values) > 2:
                    if rows[0] in data:
                        data[rows[0]].append(dp4_values)
                    else:
                        data[rows[0]] = [dp4_values]

    with open(out_file, 'w') as fout:
        fout.write('\t'.join(['gen', 'ref', 'alt', 'len']) + '\n')

        for k, v in data.items():
            ref = 0
            alt = 0

            for ref1, ref2, alt1, alt2 in v:
                if (ref1+ref2) >= (alt1+alt2):
                    ref += 1
                else:
                    alt += 1

            fout.write('\t'.join([k, '{:.5f}'.format(float(ref)/len(v)), '{:.5f}'.format(float(alt)/len(v)), str(len(v))]) + '\n')
