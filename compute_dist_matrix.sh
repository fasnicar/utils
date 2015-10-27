#!/bin/bash


# hclust2.py -i temp/all.metadata.species.clean.txt -o temp/out.svg --legend_file temp/legend.svg --skip_rows 1 --metadata_rows 2,3,4 --ftop 304 --f_dist_f euclidean --s_dist_f euclidean -l --fperc 99 --save_pickled_dist_matrix_f temp/euclidean_dist_features.pkl --save_pickled_dist_matrix_s temp/euclidean_dist_samples.pkl

# hclust2.py -i temp/all.metadata.species.clean.txt -o temp/out.svg --legend_file temp/legend.svg --skip_rows 1 --metadata_rows 2,3,4 --ftop 304 --f_dist_f euclidean --s_dist_f braycurtis -l --fperc 99 --save_pickled_dist_matrix_f temp/euclidean_dist_features.pkl --save_pickled_dist_matrix_s temp/braycurtis_dist_samples.pkl

# hclust2.py -i temp/all.metadata.species.clean.txt -o temp/out.svg --legend_file temp/legend.svg --skip_rows 1 --metadata_rows 2,3,4 --ftop 304 --f_dist_f euclidean --s_dist_f sbraycurtis -l --fperc 99 --save_pickled_dist_matrix_f temp/euclidean_dist_features.pkl --save_pickled_dist_matrix_s temp/sbraycurtis_dist_samples.pkl

hclust2.py -i temp/all.metadata.species.clean.txt -o temp/out.svg --legend_file temp/legend.svg --skip_rows 1 --metadata_rows 2,3,4 --ftop 304 --f_dist_f euclidean --s_dist_f lbraycurtis -l --fperc 99 --save_pickled_dist_matrix_f temp/euclidean_dist_features.pkl --save_pickled_dist_matrix_s temp/lbraycurtis_dist_samples.pkl

rm temp/out.svg temp/legend.svg