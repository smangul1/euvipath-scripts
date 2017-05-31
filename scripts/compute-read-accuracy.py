import argparse, sys

def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Compute errors for taxonomy results.')
    parser.add_argument('-b', '--bwa', default='NONE', help='BWA read assignments file.')
    parser.add_argument('-f', '--format', default='grinder', choices=['grinder', 'kraken'], help='Reads format.')
    parser.add_argument('-k', '--kraken', default='NONE', help='Kraken results file.')
    parser.add_argument('-p', '--paired', default=False, action='store_true', help='Paired end reads or not.')
    parser.add_argument('-r', '--report', default='NONE', help='Kraken report file.')
    #parser.add_argument('-o', '--output', default='results.txt', help='Output results file. Default: results.txt')
    parser.add_argument('reads', help='Reads file with ground truth. Required.')
    args = parser.parse_args()
    return args


def grinder_results(args):
	reads = open(args.reads, 'r')
	bwa = open(args.bwa, 'r')
	bwa.next()  # skip header line
	krak = open(args.kraken, 'r')

	report = open(args.report, 'r')
	rep_spes = []
	for line in report:
		splits = line.strip().split('\t')
		if len(splits) >= 4 and 'S' == splits[3]:
			rep_spes.append(splits[-1].strip())
	report.close()

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
		if kraknum[0] == readnum[0] and kraknum[1] == readnum[1]:
                	krakspe = krakline.split(';')[-1]
			#if krakspe in rep_spes:
			for repspe in rep_spes:
				if repspe in krakspe:
                			if krakspe in spe:
                	        		krakres[0] += 1.0
        	        		else:
	                        		krakres[1] += 1.0
					break
	reads.close()
	bwa.close()
	krak.close()
	return bwares, krakres, total


def kraken_results(args):
        reads = open(args.reads, 'r')
	bwalc, kraklc, bwadone, krakdone = 0,0,1,0
	bwa = open(args.bwa, 'r')
	for line in bwa:
		bwalc += 1
	bwa.close()
	krak = open(args.kraken, 'r')
	for line in krak:
		kraklc += 1
	krak.close()

        bwa = open(args.bwa, 'r')
        bwa.next()  # skip header line
        krak = open(args.kraken, 'r')
        report = open(args.report, 'r')
        rep_spes = []
        for line in report:
                splits = line.strip().split('\t')
                if len(splits) >= 4 and 'S' == splits[3]:
                        rep_spes.append(splits[-1].strip().lower())
        report.close()

        bwares, krakres, total = [0.0,0.0,0.0,0.0], [0.0,0.0,0.0,0.0], 0.0
        bwatag, kraktag, bwanum, kraknum = '', '', -1, -1
        bwaline, krakline = 'none', 'none'
	bwamiss, krakmiss = 0,0
        for line in reads:
                if not line.startswith('>'):
                        continue
		#if total > 1001000:
		#	break
		total += 1.0
		#readnum = int(line.strip().split('.')[1])
		readtag = line.strip()[1:].lower()
		readnum = int(readtag.split('.')[1])
		spe = line.strip()[1:].lower().split('_')[:2]
		if bwadone < bwalc and (bwatag == '' or bwatag[0] < readtag[0] or bwatag[2] < readtag[2] or (bwatag[0] == readtag[0] and bwanum < readnum)):
			bwadone += 1
			bwaline = bwa.next().strip().lower()
			#bwanum = int(bwaline.split('\t')[0])
			bwatag = bwaline.split('\t')[0]
			bwanum = int(bwatag.split('.')[1])
		if krakdone < kraklc and (kraktag == '' or kraktag[0] < readtag[0] or kraktag[2] < readtag[2] or (kraktag[0] == readtag[0] and kraknum < readnum)):
			krakdone += 1
			krakline = krak.next().strip().lower()
			#kraknum = int(krakline.split('\t')[0])
			kraktag = krakline.split('\t')[0]
			kraknum = int(kraktag.split('.')[1])
		if bwatag == readtag:
			bwaspe = bwaline.split('\t')[-1]
			if spe[0] in bwaspe and spe[1] in bwaspe:
				bwares[0] += 1.0
			else:
				bwares[1] += 1.0
		else:
			#if bwanum > 9999000:
			#	print bwatag, readtag
			bwamiss += 1
		if kraktag == readtag:
			krakspe = krakline.split(';')[-1]
			#if krakspe in rep_spes:
			for repspe in rep_spes:
				if repspe in krakspe:
					if spe[0] in krakspe and spe[1] in krakspe:
						krakres[0] += 1.0
					else:
						krakres[1] += 1.0 
					break
		else:
			#if kraknum > 9999000:
			#	print kraktag, readtag
			krakmiss += 1
		
	print
	print 'bwamiss:  ' + str(bwamiss)	
	print 'krakmiss: ' + str(krakmiss)
	print

        reads.close()
        bwa.close()
        krak.close()
        return bwares, krakres, total



args = parseargs()
if args.format == 'grinder':
	bwares, krakres, total = grinder_results(args)
elif args.format == 'kraken':
	bwares, krakres, total = kraken_results(args)

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
