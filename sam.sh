#!/bin/bash

samtools view -Sb ${1}.sam > ${1}.bam 
samtools sort ${1}.bam ${1}.sorted 
samtools index ${1}.sorted.bam
