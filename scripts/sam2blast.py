import sys, math


DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
MATCH, INSEQ, GAP = ['M', '='], ['I', 'S', 'H', 'X'], ['D', 'N', 'P']
def cigar_parse(genome_pos,cigar):
	pct, matched, missed, gaps, mapstart, mapend, genstart, genend = 0,0,0,0,-1,-1,genome_pos,0
	cur, done, cutoff = 0,0,0
	for ch in cigar:
                if mapstart == -1 and ch in MATCH:
                        mapstart = done
		if ch in DIGITS:
			cur = (cur*10) + int(ch)
		elif ch in MATCH:
			matched += cur
			done += cur
			cutoff = 0
			cur = 0
		elif ch in INSEQ:
			missed += cur
			done += cur
			cutoff += cur
			cur = 0
		elif ch in GAP:
			gaps += 1
			cur = 0
	genend = genstart + matched + missed
	mapend = done - cutoff
	pct = float(matched) / float(matched + missed)
	#print [pct, matched, missed, gaps, mapstart, mapend, genstart, genend]
	return [str(i) for i in [pct, matched, missed, gaps, mapstart, mapend, genstart, genend]]


try:
	sam = open(sys.argv[1], 'r')
	blast = open(sys.argv[2], 'w')
except:
	print 'Error: must specify valid readable input sam file and valid output file'
	print 'i.e. "python sam2blast.py in.sam out.m8" '
	sys.exit()

for line in sam:
	if line.startswith('@'):
		continue
	splits = line.split('\t')
	out = ['' for i in range(12)]
	pval = str(math.exp(-float(splits[4])))
	out = [splits[0], splits[2]]
	out.extend(cigar_parse(int(splits[3]), splits[5]))
	out.extend([pval, splits[4]])
	#out = [splits[0], splits[2]].extend(cigar_parse(int(splits[3]), splits[5])).extend([pval, splits[4]])
	blast.write('\t'.join(out) + '\n')
	

sam.close()
blast.close()
