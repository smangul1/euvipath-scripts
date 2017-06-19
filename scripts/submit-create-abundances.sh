#!/bin/sh
#$ -S /bin/bash
#$ -N job-create-abundances_nlapier2
#$ -cwd
#$ -o stdout-create-abundances.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

source ~/.bash_profile

time python ~/scratch/scripts/create-abundances.py data/bacteria-kraken.fna 544 1.5 1.0

