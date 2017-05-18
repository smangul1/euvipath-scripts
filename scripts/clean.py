f = open('microbes.fna', 'r')
outfile = open('microbes.fna-clean', 'w')
extrafile = open('microbes.fna-extras', 'w')  # contains eukaryotes, plasmids, organelles, chromosomes, etc
full = ''
extramode = False
for line in f:
	if line.startswith('>'):
		if full != '':
			if not extramode:
				outfile.write(full + '\n')
			else:
				extrafile.write(full + '\n')
		l = line.lower()
		if (not 'complete genome' in l) or 'chromosome' in l or 'mitochondri' in l or 'plast' in l or 'plasmid' in l:
			extramode = True
		else:
			extramode = False
		if not extramode:
			outfile.write(line)
		else:
			extrafile.write(line)
		full = ''
	else:
		full += line.strip()
if full != '':
	if not extramode:
		outfile.write(full + '\n')
	else:
		extrafile.write(full + '\n')
f.close()
outfile.close()
extrafile.close()
