#!/bin/sh
#$ -S /bin/bash
#$ -N job-accuracies_nlapier2
#$ -cwd
#$ -o stdout-accuracies.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

source ~/.bash_profile

python ~/scratch/scripts/compute-accuracies.py grinder-archaea-kraken-low-ranks.txt --base_dir results/archaea-kraken/ --bwa abundances-bwa-archaea-kraken-low.txt --metaphlan metaphlan-archaea-kraken-low-profile.txt

