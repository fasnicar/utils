#!/usr/bin/env python


from sys import argv


header = None
data_by_row = {}

with open(argv[1]) as f:
	for row in f:
		if not header:
			header = []

			for idd in [a.strip() for a in row.split('\t')[1:]]:
				data_by_row[idd] = []
				header.append(idd)
		else:
			for k, v in zip(header, [a.strip() for a in row.split('\t')[1:]]):
				data_by_row[k].append(v)

with open(argv[1][:argv[1].rfind('.')]+'.bin', 'w') as f:
	for k, v, in data_by_row.iteritems():
		f.write('>'+k+'\n'+''.join(v)+'\n\n')
