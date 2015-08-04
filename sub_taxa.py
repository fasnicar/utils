#!/usr/bin/env python


from sys import argv
from subprocess import call


try:
    tree = argv[1]
    taxa = argv[2]
    rtaxa = int(argv[3])
except:
    print "py utils.py <tree_file> <taxa_file> <taxa_row>"
    print "    taxa_row should be 1 for phylophlan/data/ppafull.tax.txt or 31 for phylophlan/input/bigbigtree_taxa.txt"

print "Tree file:", tree
print "Taxa file:", taxa
print "Taxa row:", rtaxa

taxad = {}
with open(taxa, 'r') as f:
    for r in f.readlines()[1:]:
        gid = r.split('\t')[0].strip()
        taf = r.split('\t')[rtaxa].strip()
        taxad[gid] = taf

for gid, taf in taxad.iteritems():
    call(['sed', '-i', 's/'+gid+'/'+gid+'_'+taf+'/g', tree])
    # print(' '.join(['sed', '-i', '"s/'+gid+'/'+gid+'_'+taf+'/g"', tree]))
