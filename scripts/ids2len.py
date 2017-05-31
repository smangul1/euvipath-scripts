import sys


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
	outfile = open('ids2len.txt', 'w')

genlens, curtag = {}, ''
for line in ref:
        if line.startswith('>'):
                curtag = find_taxid(line.strip().split(' ')[0][1:])
                if curtag in genlens:
                        print 'Warning: TaxID ' + curtag + ' occurrs twice in reference'
                else:
                        genlens[curtag] = 0
        else:
                genlens[curtag] += len(line.strip())

for gen in genlens.keys():
	outfile.write(gen + ':' + str(genlens[gen]) + '\n')

ref.close()
outfile.close()
