#!/bin/sh
#$ -S /bin/bash
#$ -N job-unbzip_nlapier2
#$ -cwd
#$ -o stdout-unbzip.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=1G,h_rt=22:00:00

#bzip2 -dk ~/scratch/data/hmp/*.bz2
#tar  -xvf ~/scratch/data/hmp/*.tar
python ~/scratch/scripts/untar.py ~/scratch/data/hmp/
