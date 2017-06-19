import sys, argparse, operator


def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Compute abundance estimations for species in a sample.')
    parser.add_argument('kraken', help='Kraken results file. Required.')
    parser.add_argument('report', help='Kraken report file. Required.')
    parser.add_argument('--abundances', default='abundances.txt', help='Output abundances file. Default: abundances.txt')
    args = parser.parse_args()
    return args


AB_CUTOFF = 0.0
args = parseargs()

report = open(args.report, 'r')
rep_spes = []
for line in report:
        splits = line.strip().split('\t')
        if len(splits) >= 4 and 'S' == splits[3]:
                rep_spes.append(splits[-1].strip())
report.close()

spe2abs, total = {}, 0.0
results = open(args.kraken, 'r')
for line in results:
	krakspe = line.split(';')[-1]
	for repspe in rep_spes:
		if repspe in krakspe:
			total += 1.0
			if krakspe in spe2abs:
				spe2abs[krakspe] += 1.0
			else:
				spe2abs[krakspe] = 1.0
			break
results.close()
for spe in spe2abs.keys():
	spe2abs[spe] /= total
	spe2abs[spe] *= 100.0

abundances = open(args.abundances, 'w')
sorted_spe2abs = sorted(spe2abs.items(), key=operator.itemgetter(1), reverse=True)
abundances.write('Abundances by Species:\n')
for line in sorted_spe2abs:
        desc = line[0].strip()
        if line[1] > AB_CUTOFF:
                abundances.write(str(desc) + '\t' + str(line[1]) + '\n')
abundances.close()
#
