#!/bin/sh
#$ -S /bin/bash
#$ -N job-filter_nlapier2
#$ -cwd
#$ -o stdout-filter.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

python qualityfilter.py matches-microbes-aa-all.m8 90.0 31

