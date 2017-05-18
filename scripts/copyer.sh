#!/bin/sh
#$ -S /bin/bash
#$ -N job_copy_nlapier2
#$ -cwd
#$ -o stdout-copy.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=12:00:00

cp microbes.faa bak/microbes.faa

