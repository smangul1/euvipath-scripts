#!/bin/sh
#$ -S /bin/bash
#$ -N job-diamond-2_nlapier2
#$ -cwd
#$ -o stdout-dmnd-2.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=50G,h_rt=24:00:00

#./diamond blastx -d ../../data/viruses-aa.dmnd -q ../../data/SRS019120.denovo_duplicates_marked.trimmed.2.fastq -o matches-aa-2.m8
./diamond blastx -d ../../data/microbes-aa.dmnd -q ../../data/SRS019120.denovo_duplicates_marked.trimmed.2.fastq -o matches-microbes-aa-2.m8

