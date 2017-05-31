from Bio import Entrez
from Bio import SeqIO
import argparse
import numpy as np
import operator
import sys
import time


AB_CUTOFF = 0#.0001
READ_CUTOFF = 10
NUM2NAME = {}


def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
    parser.add_argument('bwa', help='BWA abundances results file. Required.')
    parser.add_argument('ids2len', help='File mapping tax IDs to genome length. Required.')
    parser.add_argument('spe2ids', help='File mapping species names to tax IDs. Required.')
    parser.add_argument('--abundances', default='abundances.txt', help='Output abundances file. Default: abundances.txt')
    parser.add_argument('--assignments', default='assigned_reads.txt', help='Read classification file.')
    parser.add_argument('--paired', action='store_true', default=False, help='Use if reads are paired end.')
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


def find_int(readnum):
	original = readnum
	if readnum.startswith('>'):
		readnum = readnum[1:]
	for splitter in ['.', '/']:
		if splitter in readnum:
			readnum = readnum.split(splitter)[1]
	num = filter(str.isdigit, readnum)
	NUM2NAME[num] = original
	return int(num)


args = parseargs()
infile = open(args.bwa, 'r')
outfile = open(args.abundances, 'w')
reflens = open(args.ids2len, 'r')
refs2i = open(args.spe2ids, 'r')
rdout = open(args.assignments, 'w')

print 'Reading genome lengths file...'
genlens = {}
for line in reflens:
	splits = line.strip().split(':')
	genlens[splits[0]] = int(splits[1])
reflens.close()
print 'Done reading genome lengths file.'

ids, ids2abs, spe2id, ids2spe, spe2abs = [], {}, {}, {}, {}
prev_read_num, prev_tag, prev_count, ignore = '', '', 0.0, False
multimapped, read_assignments, ids2reads, read_ordering = {}, {}, {}, []
lc = 0
print 'Reading sam file...'
for line in infile:
	lc += 1
	if lc % 1000000 == 0:
		print 'Done reading ' + str(lc) + ' lines of sam file'
	if line.startswith('@'):
		continue
	splits = line.split('\t')
	tag = find_taxid(splits[2])
	if tag == '*':
		continue
	#read_num = int(splits[0])
	read_num = splits[0]
	read_ordering.append(read_num)
	if read_num == prev_read_num and tag == prev_tag:
		pass
		#if prev_count < 2.0 and args.paired == True:
		#	prev_count += 1.0
	elif read_num == prev_read_num and tag != prev_tag:
		ignore = True
		strnum = str(prev_read_num)
		if strnum not in multimapped:
			multimapped[strnum] = [prev_tag]
		else:
			multimapped[strnum].append(prev_tag)
		prev_tag = tag
	else:
		if not(prev_read_num == '' or ignore == True):
			read_assignments[prev_read_num] = [prev_tag]
			if prev_tag not in ids2reads:
				ids2reads[prev_tag] = [prev_read_num]
			else:
				ids2reads[prev_tag].append(prev_read_num)
			if prev_tag not in ids:
				ids.append(prev_tag)
			if prev_tag in ids2abs:
				ids2abs[prev_tag] += prev_count
			else:
				ids2abs[prev_tag] = prev_count
		elif ignore == True:
			multimapped[prev_read_num].append(prev_tag)
                prev_read_num = read_num
                prev_tag = tag
                prev_count = 1.0
                ignore = False
infile.close()
print 'Done reading sam file.'

if not(prev_read_num == '' or ignore == True):
	read_assignments[prev_read_num] = [prev_tag]
	if prev_tag not in ids2reads:
                ids2reads[prev_tag] = [prev_read_num]
        else:
                ids2reads[prev_tag].append(prev_read_num)
        if prev_tag not in ids:
                ids.append(prev_tag)
       	if prev_tag in ids2abs:
                ids2abs[prev_tag] += prev_count
       	else:
                ids2abs[prev_tag] = prev_count
elif ignore == True:
	multimapped[read_num].append(prev_tag)

print 'Deleting species/reads with insufficient evidence...'
for spe in spe2id.keys():
        if not (spe in spe2abs):
                spe2abs[spe] = 0.0
        for taxid in spe2id[spe]:
                if taxid in ids2abs:
                        spe2abs[spe] += ids2abs[taxid]
for spe in spe2abs:
	if spe2abs[spe] < READ_CUTOFF:
		for taxid in spe2abs[spe]:
			if taxid in ids2abs:
				for read in ids2reads[taxid]:
					del read_assignments[read]
				ids2abs[taxid] = 0
for taxid in ids:
	if taxid in ids2abs and ids2abs[taxid] == 0:
		del ids2abs[taxid]
print 'Done deleting species/reads.'

print 'Assigning multimapped reads...'
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
				added[key] += 1.0 #2.0
			else:
				added[key] = 1.0 #2.0
			break
		else:
			randnum -= ab
		
for key in added.keys():
	val = added[key]
	ids2abs[key] += val
print 'Multimapped reads assigned.'

for taxid in ids2abs.keys():
	ids2abs[taxid] /= genlens[taxid]  # normalize by genome length

total_ab = 0.0
for taxid in ids2abs.keys():
	total_ab += float(ids2abs[taxid])

for taxid in ids2abs.keys():
	ids2abs[taxid] = float(ids2abs[taxid]) * 100.0 / total_ab  # normalize abundances
sorted_ids2abs = sorted(ids2abs.items(), key=operator.itemgetter(1), reverse=True)

print 'Reading species to taxids file...'
for line in refs2i:
	splits = line.strip().split(':')
	taxids = splits[-1].split(' ')
	spe2id[':'.join(splits[:-1])] = taxids
	for taxid in taxids:
		ids2spe[taxid] = splits[0]
refs2i.close() 
print 'Done reading species to taxids file.'

spe2abs = {}
for spe in spe2id.keys():
	if not (spe in spe2abs):
		spe2abs[spe] = 0.0
	for taxid in spe2id[spe]:
		if taxid in ids2abs:
			spe2abs[spe] += ids2abs[taxid]
sorted_spe2abs = sorted(spe2abs.items(), key=operator.itemgetter(1), reverse=True)

print 'Computing read assignments to species...'
for read in read_assignments.keys():
	read_assignments[read].append(ids2spe[read_assignments[read][0]])
print 'Done computing read assignments to species.'

print 'Writing read assignments...'
#sorted_readassign = [str(j) for j in sorted([find_int(i) for i in read_assignments.keys()])]
#rdout = open(args.assignments, 'w')
rdout.write('Read number\tNCBI TaxID\tSpecies\n')
prevline = ''
for read in read_ordering:
	#if read not in read_assignments.keys():
	#	continue
	try:
		read_assignments[read]
	except:
		continue
	line = read + '\t' + '\t'.join(read_assignments[read]) + '\n'
	if line == prevline:
		continue
	if args.paired == False:
		rdout.write(line)
	else:
		rdout.write(read + '/1\t' + '\t'.join(read_assignments[read]) + '\n')
		rdout.write(read + '/2\t' + '\t'.join(read_assignments[read]) + '\n')
	prevline = line
rdout.close()
print 'Done writing read assignments.'

print 'Writing genome and species abundances...'
outfile.write('Abundances by Species:\n')
for line in sorted_spe2abs:
	desc = line[0]
	if line[1] > AB_CUTOFF:
		outfile.write(str(desc) + '\t' + str(line[1]) + '\n')

outfile.write('\n\nAbundances by NCBI Taxonomic ID:\n')
for line in sorted_ids2abs:
	desc = line[0]
	if '|' in desc:
		desc = desc.split('|')[0]
	if line[1] > AB_CUTOFF:
		outfile.write(str(desc) + '\t' + str(line[1]) + '\n')
outfile.close()
print 'Done.'
#
