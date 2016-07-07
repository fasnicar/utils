#!/usr/bin/env python


from glob import iglob
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC


faas = iglob('*.faa')

for faa in faas:
    print faa

    lst = []

    with open(faa, 'rU') as f:
        for record in SeqIO.parse(f, "fasta"):
            lst.append(SeqRecord(Seq(record.seq.tostring().replace('-', ''), IUPAC.protein), id=record.id, name=record.name, description=record.description))

    with open(faa[:faa.find('.')]+'_nogaps.faa', 'w') as f:
        SeqIO.write(lst, f, 'fasta')
