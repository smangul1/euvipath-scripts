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


ref, mphlan = '', ''
try:
	ref = open(sys.argv[1], 'r')
	mphlan = open(sys.argv[2], 'r')
except:
	print 'Error: must specify valid reference database and metaphlan markers file'
	print 'i.e. python compute-intersect.py ref.fa markers.fa'
	sys.exit()
try:
	outfile = open(sys.argv[3], 'w')
except:
	print 'Valid outfile not specified; writing output to ref_intersect.fa'
	outfile = open('ref_intersect.fa', 'w')

metalist, write = [], False

lc = 0
for line in mphlan:
	if not line.startswith('>'):
		continue
	if 'GeneID' in line:
		break
	lc += 1
	if lc % 100000 == 0:
		print str(lc) + ' metaphlan lines read'
	taxid = find_taxid(line.strip()[1:]) #line.split('|')[3]
	metalist.append(taxid)
	#if taxid not in metalist:
	#	metalist.append(taxid)
print 'Removing duplicates...'
metalist = list(set(metalist))

lc = 0
for line in ref:
	lc += 1
	if lc % 100000 == 0:
		print str(lc) + ' reference lines read'
	if not line.startswith('>') and write == False:
		continue
	elif not line.startswith('>') and write == True:
		outfile.write(line.upper())
	else:
		taxid = line.split('|')[0][1:]
		if taxid in metalist:
			write = True
			outfile.write(line)
		else:
			write = False

ref.close()
mphlan.close()
outfile.close()
