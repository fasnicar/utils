#!/bin/bash


for i in $(ls -d */ | grep -v ".bkp/$"); do
# for i in CA_C10006IS2084FE_t1M15 CA_C10006IS2087FE_t2M15 CA_C10006IS2091FE_t3M15 CA_C10006IS2095FE_t5M16 CA_C10006MS2082SK_t0M15 CA_C10006IS2085SA_t1M15 CA_C10006IS2088SA_t2M15 CA_C10006IS2095FE_t4M15 CA_C10006MS2079SA_t0M15; do
    cd ${i}
    echo ${i}
    # samtools mpileup ${i}${i::-1}_sorted.bam -uf ../all.fna | bcftools call -c - -o ${i}${i::-1}.vcf
    # samtools mpileup ${i}/B1886_${i}_sorted.bam -uf ../B1886.fna | bcftools call -c - -o ${i}/B1886_${i}.vcf
    # samtools mpileup ${i}/B1897_${i}_sorted.bam -uf ../B1897.fna | bcftools call -c - -o ${i}/B1897_${i}.vcf

    # for b in B1886 B1888 B1889 B1890 B1891 B1892 B1893 B1897 B1898 B1899 B1900; do
    for b in $(ls *_sorted.bam | grep -v "^CA_"); do
        c=`echo ${b} | rev | cut -f2- -d'_' | rev`
        d=`echo ${b} | cut -f1 -d'_'`

        if [ ! -f ${c}.vcf ]; then
            touch ${c}.vcf
            echo ${b}
            samtools mpileup ${b} -uf /scratchCM/tmp_projects/Caritro_genomes_Parma/${d}.fna | bcftools call -c - -o ${c}.vcf
            grep -v "INDEL;" ${c}.vcf > ${c}.indel.vcf
        fi
    done

    cd ../
done

# for i in $(ls -d */*.vcf); do
# for i in CA_C10006IS2084FE_t1M15 CA_C10006IS2087FE_t2M15 CA_C10006IS2091FE_t3M15 CA_C10006IS2095FE_t5M16 CA_C10006MS2082SK_t0M15 CA_C10006IS2085SA_t1M15 CA_C10006IS2088SA_t2M15 CA_C10006IS2095FE_t4M15 CA_C10006MS2079SA_t0M15; do
# for i in $(ls */B*.vcf); do
#     echo ${i}
#     grep -v "INDEL;" ${i}/${i}.vcf > ${i}/${i}.indel.vcf
#     grep -v "INDEL;" ${i}/B1886_${i}.vcf > ${i}/B1886_${i}.indel.vcf
#     grep -v "INDEL;" ${i}/B1897_${i}.vcf > ${i}/B1897_${i}.indel.vcf
#     grep -v "INDEL;" ${i} > ${i::-3}indel.vcf
# done
