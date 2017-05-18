#!/bin/sh
#$ -S /bin/bash
#$ -N job_unzip_nlapier2
#$ -cwd
#$ -o stdout-unzip.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

bzip2 -dk ../*.bz2 -c > microbes.fna

