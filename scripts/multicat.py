import glob, sys, subprocess

for i in range(1,len(sys.argv)):
	indir = sys.argv[i]
	if not indir.endswith('/'):
		indir += '/'
	catlist, out = ['cat'], indir+'cat.out'
	for fname in glob.glob(indir + '*'):
		catlist.append(fname)
	catlist.extend(['>', indir+'cat.out'])
	#print catlist
	subprocess.call(' '.join(catlist), shell=True)
#
