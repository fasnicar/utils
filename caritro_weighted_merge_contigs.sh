#!/bin/bash



for d in $(ls -d */ | grep -v ".bkp/$"); do
    cd ${d}

    for i in $(ls G*.snprate); do
        #if [ ! -f ${i}.old ]; then
            l=`cat ${i} | wc -l`

            if [[ $l -gt 2 ]]; then
                echo "  ${i}"
                python ../caritro_weighted_merge_contigs.py ${i}
                mv ${i} ${i}.old
                mv ${i}.new ${i}
            fi
        #fi
    done
    
    cd ../
done
