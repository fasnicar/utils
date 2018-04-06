#!/bin/bash


# compute summary stats
for i in $(ls -d */); do
    j=`ls -t ${i}*.fastq.bz2 | head -n1 | cut -f1 -d'.'`

    if [ ! -f ${j}_summary.stats ]; then
        cat_stats.py -i ${i} -o ${j}_summary.stats
    fi
done
