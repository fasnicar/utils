#!/usr/bin/env python


from re import compile


regex  = compile('s__')

babies = ['MV_FEI1_t1Q14.txt',
          'MV_FEI2_t1Q14.txt',
          'MV_FEI3_t1Q14.txt',
          'MV_FEI4_t1Q14.txt',
          'MV_FEI4_t2J15.txt', # need to be change with either Q or M
          'MV_FEI5_t1Q14.txt',
          'MV_FEI5_t2Q14.txt',
          'MV_FEI5_t3Q15.txt']
moms = ['MV_FEM1_t1Q14.txt',
        'MV_FEM2_t1Q14.txt',
        'MV_FEM3_t1Q14.txt',
        'MV_FEM4_t1Q14.txt',
        'MV_FEM4_t2J15.txt', # need to be change with either Q or M 
        'MV_FEM5_t1Q14.txt',
        'MV_FEM5_t2Q14.txt',
        'MV_FEM5_t3Q15.txt']

# print babies
# print moms

dic = {}

# read MP2 analyses
for m in babies + moms:
    bugs = set()

    with open(m) as f:
        for row in f.readlines()[1:]:
            srow = row.strip().split()[0].split('|')
            abu = float(row.strip().split()[1])

            if (len(srow) > 6) and (abu > 0.05):
                bugs |= set(srow[6])

    dic[m] = list(bugs)

# find shared bugs
for b in babies:
    for m in moms:
        s_bugs = []
	moms_list = []

        for bug in dic[b]:
            if bug in dic[m]:
                # s_bugs.append(regex.sub('', bug).replace('_', ' '))
                s_bugs.append(bug)

    	print b, m, len(s_bugs), len(dic[b]), len(dic[m]), len(s_bugs)/float(len(dic[b])+len(dic[m])-len(s_bugs))
        # print str(len(s_bugs)/float(len(dic[b])+len(dic[m])-len(s_bugs)))+'\t',
    print

    # compute norm. measure

# write output matrix

