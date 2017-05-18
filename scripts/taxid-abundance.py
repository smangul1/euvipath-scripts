import sys

def find_taxid(tag):
        if not '|' in tag:
                return tag
        else:
                splits = tag.split('|')
                for sp in splits:
                        if '_' in sp:
                                return sp
        return tag

try:
	infile = open(sys.argv[1], 'r')
	taxid = sys.argv[2]
except:
	print 'Error: must provide grinder reads input file and TaxID to compute read abunance for'
	print 'i.e. "python taxid-abundance.py grinder-reads.fa NC_020843.1'
	sys.exit()

total, match = 0.0, 0.0
for line in infile:
	if not line.startswith('>'):
		continue
	total += 1.0
	tag = find_taxid(line.split(' ')[1])
	if tag == taxid:
		match += 1.0

infile.close()
print 'Read abundance of ' + taxid + ': ' + str(match/total)
#
