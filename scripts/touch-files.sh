#!/bin/sh
#$ -S /bin/bash
#$ -N job-touchfiles_nlapier2
#$ -cwd
#$ -o stdout-touch.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=1G,h_rt=12:00:00
find . -type f -exec touch {} \;
