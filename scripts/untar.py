import glob, sys, subprocess, shlex

try:
	indir = sys.argv[1]
except:
	print 'Must specify input directory'
	sys.exit()

if not indir.endswith('/'):
	indir += '/'
for fname in glob.glob(indir + '*.bz2'):
	print fname
	subprocess.call(shlex.split('bzip2 -dk ' + fname))
for fname in glob.glob(indir + '*.tar'):
	print fname
	subprocess.call(shlex.split('tar -xvf ' + fname))
#
