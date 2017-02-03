#!/usr/bin/env python


from sys import argv
from sys import exit
from subprocess import call


try:
    tree = argv[1]
    taxa = argv[2]
    ctaxa = int(argv[3])
    sep = argv[4]
except:
    print "py utils.py <tree_file> <taxa_file> <taxa_col> <sep>"
    print "    taxa_col should be 1 for phylophlan/data/ppafull.tax.txt or 31 for phylophlan/input/bigbigtree_taxa.txt"
    exit(1)

print "Tree file:", tree
print "Taxa file:", taxa
print "Taxa col:", ctaxa
print "Sep:", sep

taxad = {}

with open(taxa, 'r') as f:
    for r in f.readlines()[1:]:
        gid = r.split('\t')[0].strip()
        taf = r.split('\t')[ctaxa].strip()
        taxad[gid] = taf

for gid, taf in taxad.iteritems():
    call(['sed', '-i', 's/'+gid+'/'+taf+sep+gid+'/g', tree])
    # print(' '.join(['sed', '-i', '"s/'+gid+'/'+gid+'_'+taf+'/g"', tree]))
