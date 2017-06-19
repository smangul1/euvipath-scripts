import argparse, subprocess, sys

def parseargs():    # handle user arguments
    parser = argparse.ArgumentParser(description='Run BWA mem for specified references and indices.')
    parser.add_argument('--index', nargs='+', help='One or more BWA index base paths.')
    parser.add_argument('--index_base', default='NONE', help='Base directory for index files.')
    parser.add_argument('--paired', default=False, action='store_true', help='Use if reads are paired-end.')
    parser.add_argument('--reads', nargs='+', help='Reads files to map to with BWA.')
    parser.add_argument('--reads_base', default='NONE', help='Base directory for reads files.')
    args = parser.parse_args()
    return args

args = parseargs()
if args.index == None or args.reads == None:
	print 'Must specify both index/indices and reference(s)'
	sys.exit()

paired = ''
if args.paired:
	paired = ' -p'
if args.index_base != 'NONE':
	if not args.index_base.endswith('/'):
		args.index_base += '/'
	for i in range(len(args.index)):
		if args.index[i].startswith('/'):
			args.index[i] = args.index[i][1:]
		args.index[i] = args.index_base + args.index[i]
if args.reads_base != 'NONE':
	if not args.reads_base.endswith('/'):
		args.reads_base += '/'
	for i in range(len(args.reads)):
		if args.reads[i].startswith('/'):
			args.reads[i] = args.reads[i][1:]
		args.reads[i] = args.reads_base + args.reads[i]

for index in args.index:
	for reads in args.reads:
		indname = index.split('/')[-1].split('.')[0]
		readsname = reads.split('/')[-1].split('.')[0]
		cmd = ' '.join(['bwa mem -a' + paired, index, reads, '>', 'bwa-'+indname+'-'+readsname+'.sam'])
		#print cmd
		#print shlex.split(cmd)
		subprocess.call(cmd, shell=True)

