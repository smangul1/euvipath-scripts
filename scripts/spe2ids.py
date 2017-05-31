import sys
from Bio import Entrez


def find_taxid(tag):
        if not '|' in tag:
                return tag
        else:
                splits = tag.split('|')
                for sp in splits:
                        if '_' in sp:
                                return sp
        return tag


try:
	ref = open(sys.argv[1], 'r')
except:
	print 'Error: Must specify reference database'
	sys.exit()
try:
	outfile = open(sys.argv[2], 'w')
except:
	outfile = open('spe2ids.txt', 'w')

spe2ids = {}
for line in ref:
	if not line.startswith('>'):
		continue
	splits = line.strip().split(' ')
	taxid = find_taxid(splits[0][1:])
	spe = ' '.join(splits[1:])
	if spe in spe2ids:
		spe2ids[spe].append(taxid)
	else:
		spe2ids[spe] = [taxid]

for spe in spe2ids.keys():
	outfile.write(spe + ':' + ' '.join(spe2ids[spe]) + '\n')

ref.close()
outfile.close()
