#!/bin/sh
#$ -S /bin/bash
#$ -N job-dl-archaea_nlapier2
#$ -cwd
#$ -o stdout-dl-archaea.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

source ~/.bash_profile

perl download_archaea.pl

