#!/bin/bash

bowtie2-build ${1}.fna ${1}
bowtie2 -x ${1} -U ${2}.fastq -S ${2}.sam
