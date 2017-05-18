#from Bio import Entrez
import numpy as np
import sys

def find_species(taxid):
	handle = Entrez.efetch(db='nucleotide', id=[taxid], rettype='gb', retmode='text')
        line = ''
        while 'ORGANISM' not in line:
                line = handle.readline().strip()
        species = (' '.join(line.split(' ')[1:])).strip()
	return species

arg, size, mu, sd = '', 0, 0.0, 0.0
try:
	arg = sys.argv[1]
	size = int(sys.argv[2])
	mu = float(sys.argv[3])
	sd = float(sys.argv[4])
except:
	print 'Must provide valid input file, # of organisms, mean, and standard deviation' 
	print 'i.e. "python create-abundances.py in.fa 40 1.0 2.0" '
	sys.exit()

with open(arg, 'r') as infile:
	names = []
	for line in infile:
		if line.startswith('>'):
			names.append(line.split(' ')[0][1:])
	
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
	
	outfile = open('abundance-file-grinder.txt', 'w')
	for i in range(len(abundances)):
		outfile.write(selected[i].strip() + '\t' + str(abundances[i]) + '\n')
	outfile.close()
#
