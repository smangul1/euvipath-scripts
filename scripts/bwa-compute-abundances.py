from Bio import Entrez
from Bio import SeqIO
import numpy as np
import operator
import sys
import time

CUTOFF = 0.0#0.001

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
	if '.' not in fname or fname.split('.')[1] not in ['sam']:
		raise Exception
	ref = sys.argv[2]
	if '.' not in ref or ref.split('.')[1] not in ['fa', 'fna', 'fasta']:
		raise Exception
	ext = fname.split('.')[1]
	infile = open(fname, 'r')
	refdb = open(ref, 'r')
except:
	print 'Error: must specify valid .sam file to read and .fa/.fna/.fasta reference database'
	sys.exit()
abundances = 'abundances.txt'
try:
	abundances = sys.argv[3]
except:
	abundances = 'abundances.txt'
outfile = open(abundances, 'w')

genlens, curtag = {}, ''
for line in refdb:
	if line.startswith('>'):
		curtag = find_taxid(line.split(' ')[0][1:])
		if curtag in genlens:
			print 'Warning: TaxID ' + curtag + ' occurrs twice in reference'
		else:
			genlens[curtag] = 0
	else:
		genlens[curtag] += len(line.strip())

ids, ids2abs, spe2id, spe2abs = [], {}, {}, {}
prev_read_num, prev_tag, prev_count, ignore = 0, '', 0.0, False
multimapped, read_assignments = {}, {}
lc = 0

for line in infile:
	lc += 1
	if lc % 100000 == 0:
		print 'Done reading ' + str(lc) + ' lines'
	if line.startswith('@'):
		continue
	splits = line.split('\t')
	tag = find_taxid(splits[2])
	read_num = int(splits[0])
	if read_num == prev_read_num and tag == prev_tag:
		if prev_count < 2.0:
			prev_count += 1.0
	elif read_num == prev_read_num and tag != prev_tag:
		ignore = True
		strnum = str(prev_read_num)
		if strnum not in multimapped:
			multimapped[strnum] = [prev_tag]
		else:
			multimapped[strnum].append(prev_tag)
		prev_tag = tag
	else:
		if not(prev_read_num == 0 or ignore == True):
			read_assignments[str(prev_read_num)] = [prev_tag]
			if prev_tag not in ids:
				ids.append(prev_tag)
			if prev_tag in ids2abs:
				ids2abs[prev_tag] += prev_count
			else:
				ids2abs[prev_tag] = prev_count
		elif ignore == True:
			multimapped[str(prev_read_num)].append(prev_tag)
                prev_read_num = read_num
                prev_tag = tag
                prev_count = 1.0
                ignore = False

if not(prev_read_num == 0 or ignore == True):
	read_assignments[str(prev_read_num)] = [prev_tag]
        if prev_tag not in ids:
                ids.append(prev_tag)
       	if prev_tag in ids2abs:
                ids2abs[prev_tag] += prev_count
       	else:
                ids2abs[prev_tag] = prev_count
elif ignore == True:
	multimapped[str(read_num)].append(prev_tag)

added = {}
for read in multimapped.keys():
	randnum = np.random.random()
	options, total = {}, 0.0
	for taxid in multimapped[read]:
		if taxid not in ids2abs or taxid in options:
			continue
		ab = ids2abs[taxid]
		total += ab
		options[taxid] = ab
	if len(options.keys()) == 0:
		continue
	for key in options.keys():
		ab = options[key] / total
		if ab >= randnum:
			read_assignments[read] = [key]
			if key in added:
				added[key] += 2.0
			else:
				added[key] = 2.0
			break
		else:
			randnum -= ab
		
for key in added.keys():
	val = added[key]
	ids2abs[key] += val

for taxid in ids2abs.keys():
	ids2abs[taxid] /= genlens[taxid]  # normalize by genome length

total_ab = 0.0
for taxid in ids2abs.keys():
	total_ab += float(ids2abs[taxid])

for taxid in ids2abs.keys():
	ids2abs[taxid] = float(ids2abs[taxid]) * 100.0 / total_ab  # normalize abundances
sorted_ids2abs = sorted(ids2abs.items(), key=operator.itemgetter(1), reverse=True)

Entrez.email = 'nathanl2012@gmail.com'
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

for spe in spe2id:
	for taxid in spe2id[spe]:
		for read in read_assignments.keys():
			if taxid in read_assignments[read]:
				read_assignments[read].append(spe)

sorted_readassign = [str(j) for j in sorted([int(i) for i in read_assignments.keys()])]
rdout = open('assigned_reads.txt', 'w')
rdout.write('Read number\tNCBI TaxID\tSpecies\n')
for read in sorted_readassign:
	rdout.write(read + '/1\t\t' + '\t'.join(read_assignments[read]) + '\n')
	rdout.write(read + '/2\t\t' + '\t'.join(read_assignments[read]) + '\n')
rdout.close()


outfile.write('Abundances by Species:\n')
for line in sorted_spe2abs:
	desc = line[0]
	if line[1] > CUTOFF:
		outfile.write(str(desc) + '\t' + str(line[1]) + '\n')

outfile.write('\n\nAbundances by NCBI Taxonomic ID:\n')
for line in sorted_ids2abs:
	desc = line[0]
	if '|' in desc:
		desc = desc.split('|')[0]
	if line[1] > CUTOFF:
		outfile.write(str(desc) + '\t' + str(line[1]) + '\n')

infile.close()
refdb.close()
outfile.close()
#
