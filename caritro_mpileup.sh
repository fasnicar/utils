#!/bin/bash


for i in $(ls -d */); do
    echo ${i}
    samtools mpileup ${i}${i::-1}_sorted.bam -uf ../all.fna | bcftools call -c - -o ${i}${i::-1}.vcf
done

for i in $(ls -d */*.vcf); do
    echo ${i}
    grep -v "INDEL;" ${i} > ${i::-3}indel.vcf
done
