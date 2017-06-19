#!/bin/sh
#$ -S /bin/bash
#$ -N job-bwa-mem_nlapier2
#$ -cwd
#$ -o stdout-bwa-mem.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=15G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa

time bwa mem -a -p ~/scratch/data/bwa/viruses_15062016.fa ~/scratch/data/grinder/grinder-viruses-intersect-mutated10-reads.fa > bwa-viruses-intersect-mutated10.sam

#time bwa mem -a ~/scratch/data/bwa/ref_intersect.fa ~/scratch/data/metasub/nycsub/SRR1749599.fasta > bwa-intersect-nycsub-plague-SRR1749599-all.sam
#time bwa mem -a ~/scratch/data/bwa/ref_intersect.fa ~/scratch/data/metasub/nycsub/SRR1749599.fastq > bwa-intersect-nycsub-plague-SRR1749599-all-fastq.sam

#time bwa mem -a ~/scratch/data/bwa/eupath/fungi.fa ~/scratch/data/nycsub/SRR1749599.fasta > bwa-SRR1749599-all-fungi.sam

#time bwa mem -a -p ~/scratch/data/bwa/fungi-kraken.fa ~/scratch/data/grinder/grinder-fungi-kraken-low-reads.fa > bwa-fungi-kraken-low-paired-all.sam
#
