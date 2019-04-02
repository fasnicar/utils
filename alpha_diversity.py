# alpha diversity

import os
import numpy as np
import pandas as pd


inp_f = '/Users/francesco/Dropbox (CIBIO)/zoe/Participants metadata/metaphlan2__103507__103505-001__species.tsv'
skiprows_list = []
inp_p, inp_e = os.path.splitext(inp_f)

# load input data
print('reading: "{}"'.format(inp_f))
mpa2_profiles = pd.read_csv(inp_f, sep='\t', header=0, index_col=0, skiprows=skiprows_list)

# number of species
print('computing: "number of species"')
num_sp = {}

for r in mpa2_profiles:
    num_sp[r] = len([e for e in mpa2_profiles[r] if e > 0])

# Gini-Simpson
print('computing: "Gini-Simpson"')
gin_si = {}

for r in mpa2_profiles:
    gin_si[r] = 1 - (sum([v**2 for v in mpa2_profiles[r].values]) / (sum(mpa2_profiles[r].values) ** 2))

# Shannon
print('computing: "Shannon"')
sha_nn = {}

for r in mpa2_profiles:
    sha_nn[r] = - sum([(v / 100) * np.log((v / 100) if (v / 100) > 0 else 1) for v in mpa2_profiles[r].values])

out_f = inp_p + '__alpha_diversity' + inp_e
print('writing: "{}"'.format(out_f))

with open(out_f, 'w') as f:
    f.write('#sample_id\tnumber_of_species\tgini_simpson\tshannon\n')
    f.write('\n'.join(['{}\t{}\t{}\t{}'.format(k, v, gin_si[k], sha_nn[k]) for k, v in num_sp.items()]) + '\n')
