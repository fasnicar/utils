#!/usr/bin/env python


from sys import argv
from subprocess import call


tree = argv[1]
taxa = argv[2]

print "Tree file:", tree
print "Taxa file:", taxa

taxad = {}
with open(taxa, 'r') as f:
    for r in f.readlines()[1:]:
        gid = r.split('\t')[0]
        taf = r.split('\t')[31]
        taxad[gid] = taf

for gid, taf in taxad.iteritems():
    call(['sed', '-i', 's/'+gid+'/'+gid+'_'+taf+'/g', tree])
