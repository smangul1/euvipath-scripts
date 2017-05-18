#!/bin/sh
#$ -S /bin/bash
#$ -N job_split_nlapier2
#$ -cwd
#$ -o stdout-split.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

python split.py 100

