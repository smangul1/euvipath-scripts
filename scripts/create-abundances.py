#from Bio import Entrez
import numpy as np
import argparse, sys


def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
    parser.add_argument('reference', help='Reference FASTA format file. Required.')
    parser.add_argument('size', type=int, help='Number of TaxIDs to select. Required.')
    parser.add_argument('mean', type=float, help='Mean species abundance. Required.')
    parser.add_argument('sd', type=float, help='Standard deviation of species abundance. Required.')
    parser.add_argument('--options', default='NONE', help='Restrict species options.')
    parser.add_argument('--output', default='abundance-file-grinder.txt', help='Output file.')
    args = parser.parse_args()
    return args


def find_species(taxid):
	handle = Entrez.efetch(db='nucleotide', id=[taxid], rettype='gb', retmode='text')
        line = ''
        while 'ORGANISM' not in line:
                line = handle.readline().strip()
        species = (' '.join(line.split(' ')[1:])).strip()
	return species

args = parseargs()
size, mu, sd = args.size, args.mean, args.sd

with open(args.reference, 'r') as infile:
	names, intersect = [], []
	if args.options != 'NONE':
		with open(args.options, 'r') as optfile:
			for line in optfile:
				intersect.append(line.strip())
	for line in infile:
		if line.startswith('>'):
			if intersect == []: 
				names.append(line.split(' ')[0][1:])
				continue
			for i in intersect:
				if i in line:
					names.append(line.split(' ')[0][1:])
					break
	
	selected, species = [], []
	#Entrez.email = 'nathanl2012@gmail.com'
	for i in range(size):
		num = int(np.random.random()*len(names))
		selection = names[num]
		#sel_spe = find_species(selection)
		while selection in selected:# or sel_spe in species:
			num = int(np.random.random()*len(names))
			selection = names[num]
			#sel_spe = find_species(selection)
		selected.append(selection)
		#species.append(sel_spe)
	#print species
	#print len(species)
	#sys.exit()

	abundances = []
	for i in range(len(selected)):
		ab = np.random.lognormal(mean=mu, sigma=sd)
		abundances.append(ab)
	sum_ab = sum(abundances)
	for i in range(len(abundances)):
		abundances[i] = abundances[i] * 100.0 / sum_ab
	abundances = sorted(abundances, reverse=True)
	
	outfile = open(args.output, 'w')
	for i in range(len(abundances)):
		outfile.write(selected[i].strip() + '\t' + str(abundances[i]) + '\n')
	outfile.close()
#
