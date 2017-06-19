import sys, argparse
from Bio import Entrez


def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
    parser.add_argument('reference', help='Reference database file. Required.')
    parser.add_argument('--output', default='spe2ids.txt', help='Output species to taxids file. Default: spe2ids.txt')
    parser.add_argument('--short', type=int, default=0, help='Specify X: use first X words of species name.')
    args = parser.parse_args()
    return args


def find_taxid(tag):
        if not '|' in tag:
                return tag
        else:
                splits = tag.split('|')
                for sp in splits:
                        if '_' in sp:
                                return sp
        return tag

'''
try:
	ref = open(sys.argv[1], 'r')
except:
	print 'Error: Must specify reference database'
	sys.exit()
try:
	outfile = open(sys.argv[2], 'w')
except:
	outfile = open('spe2ids.txt', 'w')
'''

args = parseargs()
ref = open(args.reference, 'r')
outfile = open(args.output, 'w')
spe2ids = {}
for line in ref:
	if not line.startswith('>'):
		continue
	splits = line.strip().split(' ')
	taxid = find_taxid(splits[0][1:])
	if args.short < 1 or args.short > len(splits)+1:
		spe = ' '.join(splits[1:])
	else:
		spe = ' '.join(splits[1:1+args.short])
	if spe in spe2ids:
		spe2ids[spe].append(taxid)
	else:
		spe2ids[spe] = [taxid]

for spe in spe2ids.keys():
	outfile.write(spe + ':' + ' '.join(spe2ids[spe]) + '\n')

ref.close()
outfile.close()
