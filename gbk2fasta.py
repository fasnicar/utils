#!/usr/bin/env python


from Bio import SeqIO
from glob import iglob


gbk_files = iglob('*.gbk')

for gbk_file in gbk_files:
    lst = []

    print "Reading", gbk_file
    for record in SeqIO.parse(gbk_file, "genbank"):
        lst.append(record)

    print "Writing", gbk_file[:gbk_file.rfind('.')]+'.fna'
    SeqIO.write(lst, gbk_file[:gbk_file.rfind('.')]+'.fna', "fasta")
