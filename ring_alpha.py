#!/usr/bin/env python

import sys

with open(sys.argv[1]) as f:
    for row in f:
        if "ring_alpha" in row:
            lst = row.split()

            if float(lst[-1]) < 0.0:
                print '\t'.join(lst[:-1] + ['0.0'])
                continue
            
            if float(lst[-1]) > 1.0:
                print '\t'.join(lst[:-1] + ['1.0'])
                continue

            print row.strip()
        else:
            print row.strip()
