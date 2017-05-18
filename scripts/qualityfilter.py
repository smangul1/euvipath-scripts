import argparse
import sys

def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Match quality filtering for .m6 or .m8 files')
    parser.add_argument('matchfile', metavar='input-filename', type=str, help='Input .m6 or .m8 file')
    parser.add_argument('--accuracy', default=0.0, type=float, help='Accuracy of mapping cutoff, i.e. 80.0')
    parser.add_argument('--best', default=False, action='store_true', help='Only keep best mapping of a read')
    parser.add_argument('--match', default=0, type=int, help='Minimum number of matches to reference, i.e. 50') 
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='Verbose output')
    args = parser.parse_args()
    return args


#infile = ''
#try:
#	infile = sys.argv[1]
#except:
#	print "Error: must specify input m6/m8 file"
#	sys.exit()
#try:
#	acc_cutoff = float(sys.argv[2])
#except:
#	acc_cutoff = 80.0
#try:
#	match_cutoff = int(sys.argv[3])
#except:
#	match_cutoff = 31
args = parseargs()
prev = ''
outfile = args.matchfile.split('.')[0] + '-filtered.' + args.matchfile.split('.')[1]
inf = open(args.matchfile, 'r')
outf = open(outfile, 'w')
for line in inf:
	splits = line.split('\t')
	acc = float(splits[2])
	m = int(splits[3])
	if args.best:
		if prev == splits[0]:
			continue
		else:
			prev = splits[0]
	if acc >= args.accuracy and m >= args.match:
		outf.write(line)
inf.close()
outf.close()

#
