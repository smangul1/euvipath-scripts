import sys

start = 0
try:
	start = int(sys.argv[1])
except:
	print "Error: must specify starting position"
	sys.exit()

count = 0
amount = 100000
try:
	amount = int(sys.argv[2])
except:
	amount = 100000
infile = open('microbes.faa', 'r')
outfile = open('microbes2.faa', 'w')
chunk = open('chunks.faa', 'a')
for line in infile:
	if count == 0 and not line.startswith('>'):
		continue
	if line.startswith('>'):
		count += 1
	if count >= start and count <= start + amount:
		chunk.write(line)
	else:
		outfile.write(line)
infile.close()
outfile.close()
chunk.close()
#
