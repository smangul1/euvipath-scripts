from Bio import Entrez
from Bio import SeqIO
import operator
import sys
import time

CUTOFF = 0.001

def find_taxid(tag):
        if not '|' in tag:
                return tag
        else:
                splits = tag.split('|')
                for sp in splits:
                        if '_' in sp:
                                return sp
        return tag

infile, ext = '', ''
try:
	fname = sys.argv[1]
	if '.' not in fname or fname.split('.')[1] not in ['sam', 'kraken', 'm8', 'm6']:
		raise Exception
	ext = fname.split('.')[1]
	infile = open(fname, 'r')
except:
	print 'Error: must specify valid .sam, .kraken, .m8, or .m6 format file to read'
	sys.exit()
abundances = 'abundances.txt'
try:
	abundances = sys.argv[2]
except:
	abundances = 'abundances.txt'
outfile = open(abundances, 'w')

ids, ids2abs, spe2id, spe2abs = [], {}, {}, {}
count = 0.0

if ext == 'kraken':
        for line in infile:
                count += 1.0
                spe = line.strip().split(';')[-1]
		if spe in spe2abs:
			spe2abs[spe] += 1.0
		else:
			spe2abs[spe] = 1.0
	for spe in spe2abs.keys():
		spe2abs[spe] = spe2abs[spe] / count * 100.0
	sorted_spe2abs = sorted(spe2abs.items(), key=operator.itemgetter(1), reverse=True)
	outfile.write('Abundances by Species:\n')
	for line in sorted_spe2abs:
	        desc = line[0]
	        if line[1] > CUTOFF:
	                outfile.write(str(desc) + '\t' + str(line[1]) + '\n')
	infile.close()
	outfile.close()
	sys.exit()


for line in infile:
	count += 1.0
	if int(count) % 1000000 == 0:
		print 'Done reading ' + str(int(count)) + ' lines'
	if line.startswith('@'):
		continue
	if ext == 'sam':
		tag = find_taxid(line.split('\t')[2])
	else:
		tag = find_taxid(line.split('\t')[1])
	#if '|' in tag:
	#	tag = tag.split('|')[0]
	if tag not in ids:
		ids.append(tag)
	if tag in ids2abs:
		ids2abs[tag] += 1
	else:
		ids2abs[tag] = 1

for taxid in ids2abs.keys():
	ids2abs[taxid] = float(ids2abs[taxid]) * 100.0 / count
sorted_ids2abs = sorted(ids2abs.items(), key=operator.itemgetter(1), reverse=True)

Entrez.email = 'nathanl2012@gmail.com'
#handle = Entrez.efetch(db='nucleotide', id=[', '.join(ids)], rettype='fasta')
#records = list(SeqIO.parse(handle, "fasta"))
#for rec in range(len(records)):
#        species = ' '.join(records[rec].description.split(' ')[1:3])
#        if species in spe2id:
#                spe2id[species].append(ids[rec])
#        else:
#                spe2id[species] = [ids[rec]]

print 'Tax IDs found: ' + str(ids) + '\n'
for taxid in ids:
	print 'Looking up NCBI entry for: ' + taxid + ' (' + str(ids.index(taxid)+1) + '/' + str(len(ids)) + ')'
	handle = Entrez.efetch(db='nucleotide', id=[taxid], rettype='gb', retmode='text')
	line = ''
	while 'ORGANISM' not in line:
		line = handle.readline().strip()
	species = (' '.join(line.split(' ')[1:])).strip()
	print 'Species: ' + species
	if species in spe2id:
		spe2id[species].append(taxid)
	else:
		spe2id[species] = [taxid]
	time.sleep(0.33)

for spe in spe2id.keys():
	if not (spe in spe2abs):
		spe2abs[spe] = 0.0
	for taxid in spe2id[spe]:
		spe2abs[spe] += ids2abs[taxid]
sorted_spe2abs = sorted(spe2abs.items(), key=operator.itemgetter(1), reverse=True)

outfile.write('Abundances by Species:\n')
for line in sorted_spe2abs:
	desc = line[0]
	if line[1] > CUTOFF:
		outfile.write(str(desc) + '\t' + str(line[1]) + '\n')

outfile.write('\n\nAbundances by NCBI Taxonomic ID:\n')
for line in sorted_ids2abs:
	#abundance = 100.0 * float(line[1]) / count
	desc = line[0]
	if '|' in desc:
		desc = desc.split('|')[0]
	#outfile.write(str(abundance) + '\t' + str(desc) + '\n')
	if line[1] > CUTOFF:
		outfile.write(str(desc) + '\t' + str(line[1]) + '\n')

infile.close()
outfile.close()
#
