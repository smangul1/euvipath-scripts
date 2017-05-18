#!/bin/sh
#$ -S /bin/bash
#$ -N job-intersect_nlapier2
#$ -cwd
#$ -o stdout-intersect.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

python scripts/write-intersect.py ~/scratch/Kraken_db_install_scripts-master/all-kraken.fna ~/scratch/data/markers.fasta

