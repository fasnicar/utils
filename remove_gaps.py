#!/usr/bin/env python


from glob import iglob
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC


faas = iglob('*.faa')
# faas = iglob('*.aln')

for faa in faas:
    print faa

    lst = []

    with open(faa, 'rU') as f:
        for record in SeqIO.parse(f, "fasta"):
            idd = [record.id.split('_')[0]]
            idd += [faa[:faa.rfind('.')]]
            idd += record.id.split('_')[1:]
            idd = '_'.join(idd)

            lst.append(SeqRecord(Seq(record.seq.tostring().replace('-', ''), IUPAC.protein), id=idd, name=record.name, description=record.description))

    with open(faa[:faa.find('.')].replace('_', '')+'_nogaps.faa', 'w') as f:
        SeqIO.write(lst, f, 'fasta')
