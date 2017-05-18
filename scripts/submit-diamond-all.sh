#!/bin/sh
#$ -S /bin/bash
#$ -N job-diamond-all_nlapier2
#$ -cwd
#$ -o stdout-dmnd-all.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=5G,h_rt=20:00:00

source ~/.bash_profile
~/scratch/scripts/diamond blastx -d ~/scratch/data/dmnd/viruses-aa.dmnd -q ~/scratch/data/grinder/grinder-viruses-low-reads.fa -o matches-viruses-low-all.m8

