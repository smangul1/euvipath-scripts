import sys
inname = 'microbes.fna'
#inname = 'small.fna'
infile = open(inname, 'r')
numsplits = 10
try:
	numsplits = int(sys.argv[1])
except:
	numsplits = 10

parts = inname.split('.')
outfiles = [open(parts[0]+'-'+str(i)+'.'+parts[1],'w') for i in range(numsplits)]

lc = 0
for line in infile:
	if line.startswith('>'):
		lc += 1
	outfiles[lc % numsplits].write(line)

infile.close()
