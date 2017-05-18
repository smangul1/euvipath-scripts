#!/bin/sh
#$ -S /bin/bash
#$ -N job-bwa-mem_nlapier2
#$ -cwd
#$ -o stdout-bwa-mem.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa

#bwa mem ~/scratch/results/archaea-kraken/bwa/archaea-kraken.fa ~/scratch/data/grinder/grinder-archaea-kraken-low-reads.fa > bwa-archaea-kraken-low.sam

bwa mem -a ~/scratch/results/virus-res/bwa/viruses_15062016.fa ~/scratch/data/grinder/grinder-viruses-high-reads.fa > bwa-viruses-high-all.sam

