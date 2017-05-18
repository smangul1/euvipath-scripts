#!/usr/bin/python
import argparse
import os
import sys
import time
from Bio import Entrez
from Bio import SeqIO

def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Compute errors for taxonomy results.')
    parser.add_argument('grinder_ranks', help='Ground truth grinder ranks file. Required.')
    parser.add_argument('--base_dir', default='NONE', help='Base directory of all results files.')
    parser.add_argument('--bowtie', default='NONE', help='Bowtie output for metaphlan.')
    parser.add_argument('--bwa', default='NONE', help='BWA abundances results file.')
    parser.add_argument('-d', '--diamond', default='NONE', help='Diamond abundances results file.')
    parser.add_argument('-k', '--kraken', default='NONE', help='Kraken results file.')
    parser.add_argument('-m', '--metaphlan', default='NONE', help='Metaphlan results file.')
    parser.add_argument('-o', '--output', default='results.txt', help='Output results file. Default: results.txt')
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

def parse_abundances(infile, method, spe2abs):
        abundances = open(infile, 'r')
        for line in abundances:
                if len(line) < 5:  # line after species abundances
                        break
                if line.startswith('Abundances by Species:'):
                        continue
                splits = line.strip().split('\t')
                spe = splits[0]
                spe = spe.replace('-', ' ')
                short_spe = ' '.join(spe.split(' ')[:2])
                ab = float(splits[1])
                if not (spe in spe2abs):
                        if not (short_spe in spe2abs):
                                spe2abs[spe] = {method: ab}
                        else:
                                spe2abs[short_spe][method] = ab
                else:
                        spe2abs[spe][method] = ab
	return spe2abs


args = parseargs()
if args.base_dir != 'NONE':
	os.chdir(args.base_dir)
methods = []
if args.bwa != 'NONE':
        methods.append('bwa')
if args.diamond != 'NONE':
	methods.append('diamond')
if args.metaphlan != 'NONE':
	methods.append('metaphlan')
if args.kraken != 'NONE':
	methods.append('kraken')
Entrez.email = 'nathanl2012@gmail.com'

grinder = open(args.grinder_ranks, 'r')
ids, spe2id, ids2abs, spe2abs = [], {}, {}, {}
for line in grinder:
	if line.startswith('#'):
		continue
	#taxid = line.split('\t')[1].split('|')[0]
	taxid = find_taxid(line.split('\t')[1])
	ab = float(line.strip().split('\t')[2])
	if taxid in ids:
		print "Error: same taxonomic ID occurs twice in grinder file."
		sys.exit()
	ids.append(taxid)
	ids2abs[taxid] = {'grinder':ab}
grinder.close()

if args.metaphlan != 'NONE':
	metaphlan = open(args.metaphlan, 'r')
	for line in metaphlan:
		if 't__' in line or not ('s__' in line):
			continue
		info = line.strip().split('s__')[1].split('\t')
		ab = float(info[1])
		spe = ' '.join(info[0].split('_'))
		#if spe == 'Eremothecium gossypii':
		#	spe = 'Ashbya gossypii'
		#if spe == 'Vibrio phage 11895 B1':
		#	spe = 'Vibrio phage 11895-B1'
		if not (spe in spe2abs):
			spe2abs[spe] = {'metaphlan': ab}
		else:
			spe2abs[spe]['metaphlan'] = ab
	metaphlan.close()

if args.diamond != 'NONE':
	spe2abs = parse_abundances(args.diamond, 'diamond', spe2abs)
if args.bwa != 'NONE':
        spe2abs = parse_abundances(args.bwa, 'bwa', spe2abs)
if args.kraken != 'NONE':
        spe2abs = parse_abundances(args.kraken, 'kraken', spe2abs)

'''
if args.diamond != 'NONE':
	abundances = open(args.diamond, 'r')
	for line in abundances:
		if len(line) < 5:  # line after species abundances
			break
		if line.startswith('Abundances by Species:'):
			continue
		splits = line.strip().split('\t')
		spe = splits[0]
		spe = spe.replace('-', ' ')
		short_spe = ' '.join(spe.split(' ')[:2])
		ab = float(splits[1])
		if not (spe in spe2abs):
			if not (short_spe in spe2abs):
				spe2abs[spe] = {'diamond': ab}
			else:
				spe2abs[short_spe]['diamond'] = ab
		else:
			spe2abs[spe]['diamond'] = ab

if args.bwa != 'NONE':
        abundances = open(args.bwa, 'r')
        for line in abundances:
                if len(line) < 5:  # line after species abundances
                        break
                if line.startswith('Abundances by Species:'):
                        continue
                splits = line.strip().split('\t')
                spe = splits[0]
		spe = spe.replace('-', ' ')
                short_spe = ' '.join(spe.split(' ')[:2])
                ab = float(splits[1])
                if not (spe in spe2abs):
                        if not (short_spe in spe2abs):
                                spe2abs[spe] = {'bwa': ab}
                        else:
                                spe2abs[short_spe]['bwa'] = ab
                else:
                        spe2abs[spe]['bwa'] = ab
'''

#print 'Tax IDs found: ' + str(ids) + '\n'
for taxid in ids:
        #print 'Looking up NCBI entry for: ' + taxid + ' (' + str(ids.index(taxid)+1) + '/' + str(len(ids)) + ')'
        handle = Entrez.efetch(db='nucleotide', id=[taxid], rettype='gb', retmode='text')
        line = ''
        while 'ORGANISM' not in line:
                line = handle.readline().strip()
        species = (' '.join(line.split(' ')[1:])).strip()
	species = species.replace('-', ' ')
	short_spe = ' '.join(species.split(' ')[:2])
	if short_spe in spe2abs:
		species = short_spe
        #print 'Species: ' + species
        if species in spe2id:
                spe2id[species].append(taxid)
        else:
                spe2id[species] = [taxid]
        time.sleep(0.1)#0.33
#handle = Entrez.efetch(db='nucleotide', id=[', '.join(ids)], rettype='fasta')
#records = list(SeqIO.parse(handle, "fasta"))
#for rec in range(len(records)):
#	#species = ' '.join(records[rec].description.split(' ')[1:3])
#	species = ' '.join(records[rec].description.split(',')[0].split(' ')[1:])
#	if species in spe2id:
#		spe2id[species].append(ids[rec])
#	else:
#		spe2id[species] = [ids[rec]]

for spe in spe2id.keys():
	if not (spe in spe2abs):
		spe2abs[spe] = {}
	for taxid in spe2id[spe]:
		id_dict = ids2abs[taxid]
		for key in id_dict.keys():
			if key in spe2abs[spe]:
				spe2abs[spe][key] += id_dict[key]
			else:
				spe2abs[spe][key] = id_dict[key]

for spe in spe2abs.keys():
	if 'grinder' not in spe2abs[spe].keys():
		spe2abs[spe]['grinder'] = 0.0
	for m in methods:
		if m not in spe2abs[spe].keys():
			spe2abs[spe][m] = 0.0
        #if 'diamond' not in spe2abs[spe].keys() and 'diamond' in methods:
        #        spe2abs[spe]['diamond'] = 0.0
        #if 'metaphlan' not in spe2abs[spe].keys() and 'metaphlan' in methods:
        #        spe2abs[spe]['metaphlan'] = 0.0

l1err = {}
tpfptnfn = {}
for m in methods:
	l1err[m] = 0.0
	tpfptnfn[m] = [0.0, 0.0, 0.0, 0.0]#, 0.0]
for spe in spe2abs.keys():
	true_ab = spe2abs[spe]['grinder']
	for m in spe2abs[spe].keys():
		if m == 'grinder':
			continue
		ab = spe2abs[spe][m]
		l1err[m] += abs(true_ab - ab)
		#tpfptnfn[m][4] += 1.0
		if true_ab > 0.0 and ab > 0.0:
			tpfptnfn[m][0] += 1.0
		elif true_ab == 0.0 and ab > 0.0:
			tpfptnfn[m][1] += 1.0
		elif true_ab == 0.0 and ab == 0.0:
			tpfptnfn[m][2] += 1.0
		else:
			tpfptnfn[m][3] += 1.0

for m in methods:
	print '\nResults for ' + m + ':'
	print 'L1 error: ' + str(l1err[m])
	print '[TP,FP,TN,FN]: ' + str(tpfptnfn[m])
	vals = tpfptnfn[m]
	if vals[0] == 0.0 and vals[1] == 0.0:
		precision = 0.0
	else:
		precision = vals[0] / (vals[0] + vals[1])
	if vals[0] == 0.0 and vals[3] == 0.0:
		recall = 0.0
	else:
		recall = vals[0] / (vals[0] + vals[3])
	if precision == 0.0 and recall == 0.0:
		fscore = 0.0
	else:
		fscore = 2 * precision * recall / (precision + recall)
	print 'Precision/Recall: ' + str(precision) + '/' + str(recall)
	print 'F1-score: ' + str(fscore)

#print spe2abs
'''
print ids
print '\n'
print ids2abs
print '\n'
print spe2id
print '\n'
print spe2abs
print '\n'
print l1err
print '\n'
print tpfptnfn
'''
#
