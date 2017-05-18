from Bio import Entrez
import numpy as np
import sys

def find_species(taxid):
        handle = Entrez.efetch(db='nucleotide', id=[taxid], rettype='gb', retmode='text')
        line = ''
        while 'ORGANISM' not in line:
                line = handle.readline().strip()
        species = (' '.join(line.split(' ')[1:])).strip()
        return species

infile = ''
try:
	infile = sys.argv[1]
	infile = open(infile, 'r')
except:
	print 'must specify valid input fasta format reference database'
	sys.exit()

Entrez.email = 'nathanl2012@gmail.com'
species, ids = [], 0
for line in infile:
	if line.startswith('>'):
		taxid = line.split(' ')[0][1:]
		ids += 1
		if ids % 100 == 0:
			print str(ids) + ' lookups processed'
		spe = find_species(taxid)
		if spe not in species:
			species.append(spe)
		
print 'Number of species: ' + str(len(species))
print 'Number of taxonomic IDs: ' + str(ids)
#
