#!/bin/bash

# bowtie2
bowtie2-build ${1}.fna ${1}
bowtie2 -x ${1} -U ${2}.fastq -S ${2}.sam

# samtools
samtools view -Sb ${2}.sam > ${2}.bam 
samtools sort ${2}.bam ${2}.sorted 
samtools index ${2}.sorted.bam
