#!/bin/sh
#$ -S /bin/bash
#$ -N job-read-accuracies_nlapier2
#$ -cwd
#$ -o stdout-read-accuracies.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

source ~/.bash_profile

python scripts/compute-read-accuracy.py ~/scratch/kraken-data/timing/HiSeq_timing.fa -b ~/scratch/results/hiseq-timing/assigned-reads-bwa.txt -k ~/scratch/results/hiseq-timing/kraken-hiseq-timing-results.kraken -r ~/scratch/results/hiseq-timing/kraken-hiseq-timing-report.txt -f kraken
#
