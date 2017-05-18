import os
import sys


beans = "TGACTGTGTTTCTGAACAATAAATGACTTAAACCAGGTATGGCTGCCGATGGTTATCTT"

gencode = {
      'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
      'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
      'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
      'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
      'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
      'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
      'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
      'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
      'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
      'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
      'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
      'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
      'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
      'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
      'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
      'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W'}


basepairs = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}

def translate_frameshifted(sequence):
      translate = ''.join([gencode.get(sequence[3*i:3*i+3],'X') for i in range(len(sequence)//3)])
      return translate

def reverse_complement(sequence):
      reversed_sequence = (sequence[::-1])
      rc = ''.join([basepairs.get(reversed_sequence[i], 'X') for i in range(len(sequence))])
      return rc



def nucleotide2protein2(inString):
    frames = []
    framesTemp = []

    framesTemp.append(translate_frameshifted(inString[0:]))  # first frame
    framesTemp.append(translate_frameshifted(inString[1:]))  # second frame
    framesTemp.append(translate_frameshifted(inString[2:]))  # third frame
    framesTemp.append(translate_frameshifted(reverse_complement(inString)))  # negative first frame
    framesTemp.append(translate_frameshifted(reverse_complement(inString)[1:]))  # negative second frame
    framesTemp.append(translate_frameshifted(reverse_complement(inString)[2:]))  # negative third frame

    frs = [1, 2, 3, -1, -2, -3]

    for f, frame in zip(framesTemp, frs):
        if 1 == 1: #if "_" not in f:
            processedRead=f.replace(' ','')
            frames.append((processedRead, frame))
    return frames


def dumpClones(clones, outFile):
    with open(outFile, "w") as f:
        for clone in clones:
            f.write(("\t".join(["%s"] * len(clone)) + "\n") % tuple(clone))


def dumpClones2(clones, outFile):
    with open(outFile, "w") as f:
        for clone in clones:
            f.write(clone)



def getGeneType(geneName):
    """
    Hopefully, it is safe
    """
    geneType = geneName.split("|")[1].split("*")[0]
    if "-" in geneType:
        geneType = geneType.split("-")[0]
    return geneType



def getGeneType2(geneName):
    """
    Hopefully, it is safe
    """
    geneType = geneName.split("|")[1].split("*")[0]
    if "-" in geneType:
        geneType = geneType.split("-")[0]
    return geneType[:4]


def main():
	fa = ''
	aa = ''
	try:
		fa = sys.argv[1]
		aa = sys.argv[2]
	except:
		print 'Must specify valid input and output file names, i.e. "python translate.py in.fa out.aa" '
		sys.exit()
        infile = open(fa, 'r')
        outfile = open(aa, 'w')
	defline = ''
	total_frames = ['','','','','','']
	for line in infile:
		if line.startswith('>'):
			if total_frames[0] != '':
				for i in range(len(total_frames)):
					if i <= 2:
						framenum = i - 3
					else:
						framenum = i - 2
					outfile.write(defline + '_' + str(framenum) + '\n')
					outfile.write(total_frames[i] + '\n')
			defline = line.strip()
		else:
			frames = nucleotide2protein2(line.strip())
			for frame in range(len(frames)):
				total_frames[frame] += frames[frame][0]
				#outfile.write(defline + '_' + str(frame[1]) + '\n')
				#outfile.write(frame[0] + '\n')
	
        if total_frames[0] != '':
	        for i in range(len(total_frames)):
		        if i <= 2:
			        framenum = i - 3
                        else:
                                framenum = i - 2
                        outfile.write(defline + '_' + str(framenum) + '\n')
                        outfile.write(total_frames[i] + '\n')

	outfile.close()
	infile.close()


if __name__ == '__main__':
	main()

#
