#!/bin/bash


ncores='32'
pr='/CIBIO/sharedCM/metagenomes/Caritro/splitted'
po='/scratch/sharedCM/metagenomes/Caritro_genomes_Parma/mapping'
pi='/scratch/sharedCM/metagenomes/Caritro_genomes_Parma'
pt='/scratch/sharedCM/users/f.asnicar/utils'
py=python

# for s in $(ls ${pr}/*.fastq.bz2 | rev | cut -f1 -d '/' | rev | cut -f1 -d'.' | rev | cut -f2- -d'_' | rev | sort | uniq); do
for s in CA_C10009IS2141FE_t2M15; do 
    echo ${s}
    mkdir -p ${po}/${s}
    cd ${po}/${s}/

    bowtie2 -x ${pi}/base -1 <(bzcat ${pr}/${s}_R1.fastq.bz2) -2 <(bzcat ${pr}/${s}_R2.fastq.bz2) -U <(bzcat ${pr}/${s}_unpaired.fastq.bz2) -S ${s}.sam --very-sensitive-local -k 100000 --no-unal -p ${ncores} 2> ${s}.log

#    samtools view -bS ${s}.sam > ${s}.bam
#    samtools sort ${s}.bam ${s}_sorted
#    samtools index ${s}_sorted.bam

#    rm ${s}.sam ${s}.bam

#    ${py} ${pt}/bowtie2_coverage.py ${s}_sorted.bam ${pi}/
done
