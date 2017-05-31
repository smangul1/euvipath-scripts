#!/bin/sh
#$ -S /bin/bash
#$ -N job-ncbi-dl_nlapier2
#$ -cwd
#$ -o stdout-ncbi-dl.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=1G,h_rt=24:00:00

source ~/.bash_profile

python scripts/bulkNCBIDownload.py --list ~/scratch/nycsranums.txt --dlpath ~/bin/fastq-dump.2.8.0 --out ~/scratch/nycsub/ 

