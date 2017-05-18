#!/bin/sh
#$ -S /bin/bash
#$ -N job-abundances_nlapier2
#$ -cwd
#$ -o stdout-abundances.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

source ~/.bash_profile

python ~/scratch/scripts/compute-abundances.py ~/scratch/results/archaea-kraken/bwa-archaea-kraken-low.sam abundances-bwa-archaea-kraken-low.txt

