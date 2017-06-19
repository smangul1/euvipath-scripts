#!/bin/sh
#$ -S /bin/bash
#$ -N job-cat_nlapier2
#$ -cwd
#$ -o stdout-cat.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

cat bacteria/*.fna > bacteria.fna

