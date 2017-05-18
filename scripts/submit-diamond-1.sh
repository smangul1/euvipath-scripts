#!/bin/sh
#$ -S /bin/bash
#$ -N job-diamond-1_nlapier2
#$ -cwd
#$ -o stdout-dmnd-1.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=50G,h_rt=24:00:00

#./diamond blastx -d ../../data/viruses-aa.dmnd -q ../../data/SRS019120.denovo_duplicates_marked.trimmed.1.fastq -o matches-aa-1.m8
./diamond blastx -d ../../data/microbes-aa.dmnd -q ../../data/SRS019120.denovo_duplicates_marked.trimmed.1.fastq -o matches-microbes-aa-1.m8

