import argparse, sys

def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Compute errors for taxonomy results.')
    parser.add_argument('-b', '--bwa', default='NONE', help='BWA read assignments file.')
    parser.add_argument('-k', '--kraken', default='NONE', help='Kraken results file.')
    parser.add_argument('-o', '--output', default='results.txt', help='Output results file. Default: results.txt')
    parser.add_argument('reads', help='Reads file with ground truth. Required.')
    args = parser.parse_args()
    return args

args = parseargs()
reads = open(args.reads, 'r')
bwa = open(args.bwa, 'r')
bwa.next()  # skip header line
krak = open(args.kraken, 'r')

bwares, krakres, total = [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0], 0.0
bwanum, kraknum = [-1,-1], [-1,-1]
bwaline, krakline = '', ''
for line in reads:
	if not line.startswith('>'):
		continue
	total += 1.0
	readnum = [int(i) for i in line.split(' ')[0][1:].split('/')]
	spe = line.split('"')[1]
	if bwanum[0] < readnum[0] or (bwanum[0] == readnum[0] and bwanum[1] < readnum[1]):
		bwaline = bwa.next().strip()
		bwanum = [int(i) for i in bwaline.split('\t')[0].split('/')]
	if bwanum[0] == readnum[0] and bwanum[1] == readnum[1]:
		bwaspe = bwaline.split('\t')[-1]
		if bwaspe in spe or bwaline.split('\t')[-2] in line:
			bwares[0] += 1.0
		else:
			bwares[1] += 1.0
        if kraknum[0] < readnum[0] or (kraknum[0] == readnum[0] and kraknum[1] < readnum[1]):
                krakline = krak.next().strip()
                kraknum = [int(i) for i in krakline.split('\t')[0].split('/')]
        if kraknum[0] == readnum[0] and kraknum[1] == readnum[1] and (krakline.count(';') + krakline.count('ssDNA') == 6):
		krakspe = krakline.split(';')[-1]
                if krakspe in spe:
                        krakres[0] += 1.0
                else:
                        krakres[1] += 1.0
	#print readnum, spe, bwanum, bwaline.split('\t')[-1], kraknum, krakline.split(';')[-1]
	#print bwares, krakres
	#sys.exit()

print 'BWA Results:'
if bwares[0] == 0.0:
	precision, recall, fscore = 0.0, 0.0, 0.0
else:
	precision = bwares[0] / (bwares[0] + bwares[1])
	recall = bwares[0] / total
	fscore = 2.0 * precision * recall / (precision + recall)
print 'Precision: ' + str(precision)
print 'Recall/sensitivity: ' + str(recall)
print 'F-score: ' + str(fscore)
print ''

print 'Kraken Results:'
if krakres[0] == 0.0:
	precision, recall, fscore = 0.0, 0.0, 0.0
else:
	precision = krakres[0] / (krakres[0] + krakres[1])
	recall = krakres[0] / total
	fscore = 2.0 * precision * recall / (precision + recall)
print 'Precision: ' + str(precision)
print 'Recall/sensitivity: ' + str(recall)
print 'F-score: ' + str(fscore)
print ''

reads.close()
bwa.close()
krak.close()
