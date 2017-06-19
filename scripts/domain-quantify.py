import sys, argparse, glob


def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Compute domain abundances in a sample.')
    parser.add_argument('reads', help='Input reads file. Required.')
    parser.add_argument('dir', help='Directory with SAM files. Required.')
    parser.add_argument('sample', help='Sample name. Required.')
    parser.add_argument('--ignore', default='NONE', nargs='+', help='Domains to ignore. Optional.')
    parser.add_argument('--select', default='NONE', nargs='+', help='Domains to quantify. Optional.')
    parser.add_argument('--threshold', default='NONE', help='Threshold for % of bases mapped in a read. Optional.')
    args = parser.parse_args()
    return args


args = parseargs()
if args.ignore != 'NONE' and args.select != 'NONE':
	for i in args.ignore:
		if i in args.select:
			print 'Error: ' + i + ' in both ignore and select lists.'
			sys.exit()

reads = open(args.reads, 'r')
total = 0.0
if args.reads.lower().endswith('a'):
	for line in reads:
		if not line.startswith('>'):
			continue
else:
	for line in reads:
		total += 1.0
	total /= 4.0
reads.close()
print str(int(total)) + ' reads counted'

read_mappings, counts = {}, {'bacteria': 0.0, 'archaea': 0.0, 'viruses': 0.0, 'eukaryotes': 0.0, 'ambiguous': 0.0}
translate = {'ameoba': 'eukaryotes', 'crypto': 'eukaryotes', 'fungi': 'eukaryotes', 'giardia': 'eukaryotes', 'microsporidia': 'eukaryotes', 'piroplasma': 'eukaryotes', 'plasmo': 'eukaryotes', 'toxo': 'eukaryotes', 'trich': 'eukaryotes', 'nonflu_all': 'viruses'}
for fname in glob.glob(args.dir + '*' + args.sample + '*.sam'):
	if '-' not in fname:
		continue
	domain = fname.split('/')[-1].split('-')[1]
	if domain.lower() in translate:
		domain = translate[domain.lower()]
	skip = False
	if args.ignore != 'NONE':
		for i in args.ignore:
			if i == domain:
				skip = True
	if args.select != 'NONE':
		skip = True
		for i in args.select:
			if i == domain:
				skip = False
	if skip == True:
		continue
	print 'Reading: ' + fname
	print 'Domain: ' + domain
	
	sam = open(fname, 'r')
	prevtag = ''
	for line in sam:
		if line.startswith('@'):
			continue
		splits = line.split('\t')
		if splits[2] == '*' or splits[0] == prevtag:
			continue
		prevtag = splits[0]
		if prevtag in read_mappings:
			#counts['ambiguous'] += 1.0
			if len(read_mappings[prevtag]) == 1:
				counts['ambiguous'] += 1.0
				counts[read_mappings[prevtag][0]] -= 1.0
			read_mappings[prevtag].append(domain)
		else:
			read_mappings[prevtag] = [domain]
			counts[domain] += 1.0
	sam.close()

unknown = total
for key in counts.keys():
	unknown -= counts[key]
counts['unknown'] = unknown

print '\nAbundances by domain:\n'
for key in counts.keys():
	print key + ': ' + str(counts[key] / total)
#
