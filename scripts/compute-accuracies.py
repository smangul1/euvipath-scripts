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
    parser.add_argument('spe2ids', help='File mapping species to tax IDs. Required.')
    parser.add_argument('--base_dir', default='NONE', help='Base directory of all results files.')
    parser.add_argument('--bowtie', default='NONE', help='Bowtie output for metaphlan.')
    parser.add_argument('--bwa', default='NONE', help='BWA abundances results file.')
    parser.add_argument('--debug', default=False, action='store_true', help='Debug option (prints a lot)')
    parser.add_argument('--diamond', default='NONE', help='Diamond abundances results file.')
    parser.add_argument('-i', '--intersect', default='NONE', help='File to output intersection of results to.')
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
                #spe = spe.replace('-', ' ')
                #short_spe = ' '.join(spe.split(' ')[:2])
                ab = float(splits[1])
                if not (spe in spe2abs):
			assigned = False
			for fullspe in spe2abs:
				if spe in fullspe or fullspe in spe:
					spe2abs[fullspe][method] = ab
					assigned = True
			if assigned == False:
                        #if not (short_spe in spe2abs):
                        	spe2abs[spe] = {method: ab}
                        #else:
                        #        spe2abs[short_spe][method] = ab
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
ids, spe2id, ids2spe, ids2abs, spe2abs = [], {}, {}, {}, {}
refs2i = open(args.spe2ids, 'r')
for line in refs2i:
        splits = line.strip().split(':')
        #taxids = splits[1].split(' ')
        #spe2id[splits[0]] = taxids
        taxids = splits[-1].split(' ')
        spe2id[':'.join(splits[:-1])] = taxids
        for taxid in taxids:
                ids2spe[taxid] = splits[0]
refs2i.close()

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
	spe2abs[ids2spe[taxid]] = {'grinder':ab}
grinder.close()

if args.diamond != 'NONE':
	spe2abs = parse_abundances(args.diamond, 'diamond', spe2abs)
if args.bwa != 'NONE':
        spe2abs = parse_abundances(args.bwa, 'bwa', spe2abs)
if args.kraken != 'NONE':
        spe2abs = parse_abundances(args.kraken, 'kraken', spe2abs)

if args.metaphlan != 'NONE':
        metaphlan = open(args.metaphlan, 'r')
        for line in metaphlan:
                if 't__' in line or not ('s__' in line):
                        continue
                info = line.strip().split('s__')[1].split('\t')
                ab = float(info[1])
                spe = ' '.join(info[0].split('_'))
                #if spe == 'Eremothecium gossypii':
                #       spe = 'Ashbya gossypii'
                #if spe == 'Vibrio phage 11895 B1':
                #       spe = 'Vibrio phage 11895-B1'
		assigned = False
		for fullspe in spe2abs:
			accept = True
			splits = spe.split(' ')
			for split in splits:
				if split not in fullspe:
					accept = False
			if accept == True:
			#if ' '.join(spe.split(' ')[:2]) in fullspe:
				spe2abs[fullspe]['metaphlan'] = ab
				assigned = True
				break

		if assigned == False:
			spe2abs[spe] = {'metaphlan': ab}
                #if not (spe in spe2abs):
                #        spe2abs[spe] = {'metaphlan': ab}
                #else:
                #        spe2abs[spe]['metaphlan'] = ab
        metaphlan.close()

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

if args.intersect != 'NONE':
	intfile = open(args.intersect, 'w')
	for spe in spe2abs:
		write = True
		for m in methods:
			if m not in spe2abs[spe] or spe2abs[spe][m] == 0.0:
				write = False
		if write == True:
			intfile.write(spe + '\n')
	intfile.close()

if args.debug == True:
	for spe in spe2abs:
		print spe + ': ' + str(spe2abs[spe])
#
