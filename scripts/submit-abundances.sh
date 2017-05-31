#!/bin/sh
#$ -S /bin/bash
#$ -N job-abundances_nlapier2
#$ -cwd
#$ -o stdout-abundances.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=12:00:00

source ~/.bash_profile

#python ~/scratch/scripts/compute-abundances.py ~/scratch/results/archaea-kraken/bwa-archaea-kraken-low.sam abundances-bwa-archaea-kraken-low.txt
#time python ~/scratch/scripts/bwa-compute-abundances.py ~/scratch/results/nycsub/bwa-intersect-nycsub-plague-SRR1749599-all.sam ~/scratch/data/ids2len-intersect.txt ~/scratch/data/spe2ids-intersect.txt --abundances abundances-bwa-intersect-nycsub-plague-SRR1749599-filtered.txt --assignments assigned-reads-bwa-intersect-nycsub-plague-SRR1749599-filtered.txt
time python scripts/bwa-compute-abundances.py results/hiseq-timing/bwa-intersect-hiseq-all.sam data/ids2len-intersect.txt data/spe2ids-intersect.txt --abundances abundances-bwa-intersect-hiseq-filtered.txt --assignments assigned-reads-bwa-intersect-hiseq-filtered.txt

