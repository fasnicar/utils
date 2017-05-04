#!/bin/bash


ncores='8'

# pr='/CIBIO/sharedCM/metagenomes/Caritro/splitted'
pr='/scratchCM/tmp_projects/Caritro/splitted'

# po='/scratch/sharedCM/metagenomes/Caritro_genomes_Parma/mapping'
po='/scratchCM/tmp_projects/Caritro_genomes_Parma/mapping'

# pi='/scratch/sharedCM/metagenomes/Caritro_genomes_Parma'
pi='/scratchCM/tmp_projects/Caritro_genomes_Parma'

# pt='/scratch/sharedCM/users/f.asnicar/git/utils'
pt='/scratchCM/users/f.asnicar/git/utils'

py=python

# for s in $(ls ${pr}/*.fastq.bz2 | rev | cut -f1 -d '/' | rev | cut -f1 -d'.' | rev | cut -f2- -d'_' | rev | sort | uniq); do
# for s in CA_C10009IS2141FE_t2M15; do
# for s in CA_C10006IS2084FE_t1M15 CA_C10006IS2087FE_t2M15 CA_C10006IS2091FE_t3M15 CA_C10006IS2095FE_t5M16 CA_C10006MS2082SK_t0M15 CA_C10006IS2085SA_t1M15 CA_C10006IS2088SA_t2M15 CA_C10006IS2095FE_t4M15 CA_C10006MS2079SA_t0M15; do
for d in $(ls -d mapping/*/ | grep -v ".bkp/$"); do
    s=`echo ${d} | cut -f2 -d'/'`
    echo ${s}
    mkdir -p ${po}/${s}
    cd ${po}/${s}/

    # bowtie2 -x ${pi}/base -1 <(bzcat ${pr}/${s}_R1.fastq.bz2) -2 <(bzcat ${pr}/${s}_R2.fastq.bz2) -U <(bzcat ${pr}/${s}_unpaired.fastq.bz2) -S ${s}.sam --very-sensitive-local -k 100000 --no-unal -p ${ncores} 2> ${s}.log

    # samtools view -bS ${s}.sam > ${s}.bam
    # samtools sort ${s}.bam ${s}_sorted
    # samtools index ${s}_sorted.bam

    # rm ${s}.sam ${s}.bam

    for b in B1886 B1887 B1888 B1889 B1890 B1891 B1892 B1893 B1897 B1898 B1899 B1900 G000497735 G000196575 G000219455 G000007525 G001293145 G000020425 G000166315 G000196555 G000269965 G000829295 G001020255 G001020275 G000741085 G001020375 G000164965 G000165905 G000265095 G000273525 G001025135 G001281345 G000568875 G001281425 G000213865 G000220135 G000568975 G000569015 G000569035 G000569055 G000569075 G001025175 G000771705 G001010915 G000010425 G000737885 G000817995 G000173455 G000741565 G001025195 G000149165 G000771725 G001576945 G000172135 G000024445 G001042595; do
    # for b in B1886 B1888 B1889 B1890 B1891 B1892 B1893 B1897 B1898 B1899 B1900 G000497735 G000196575 G000219455 G000007525 G001293145 G000020425 G000166315; do
    # for b in G000196555 G000269965 G000829295 G001020255 G001020275 G000741085 G001020375 G000164965 G000165905 G000265095 G000273525 G001025135 G001281345 G000568875 G001281425 G000213865 G000220135 G000568975 G000569015; do
    # for b in G000569035 G000569055 G000569075 G001025175 G000771705 G001010915 G000010425 G000737885 G000817995 G000173455 G000741565 G001025195 G000149165 G000771725 G001576945 G000172135 G000024445 G001042595; do
    # for b in B1887; do
        if [ ! -f ${b}_${s}.log ] && [ ! -f ${b}_${s}.bam ] && [ ! -f ${b}_${s}_sorted.bam ]; then
            echo ${b}
            bowtie2 -x ${pi}/${b} -1 <(bzcat ${pr}/${s}_R1.fastq.bz2) -2 <(bzcat ${pr}/${s}_R2.fastq.bz2) -U <(bzcat ${pr}/${s}_unpaired.fastq.bz2) -S ${b}_${s}.sam --very-sensitive-local -k 100000 --no-unal -p ${ncores} 2> ${b}_${s}.log

            samtools view -bS ${b}_${s}.sam > ${b}_${s}.bam
            samtools sort ${b}_${s}.bam -o ${b}_${s}_sorted.bam
            samtools index ${b}_${s}_sorted.bam

            rm ${b}_${s}.sam ${b}_${s}.bam
        fi
    done

    # ${py} ${pt}/bowtie2_coverage.py ${s}_sorted.bam ${pi}/
done
