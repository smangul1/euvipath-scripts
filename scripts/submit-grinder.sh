#!/bin/sh
#$ -S /bin/bash
#$ -N job-grinder_nlapier2
#$ -cwd
#$ -o stdout-grinder.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

source ~/.bash_profile
#grinder -reference_file ~/scratch/data/archaea-kraken.fa -total_reads 1000000 -abundance_file ~/scratch/data/grinder/abundance-archaea-kraken-low.txt -read_dist 150 normal 15 -insert_dist 270 -base_name grinder-archaea-kraken-low
grinder -reference_file ~/scratch/data/viruses_15062016.fa -total_reads 1000000 -abundance_file ~/scratch/data/grinder/abundance-viruses-intersect.txt -read_dist 150 normal 15 -insert_dist 270 -base_name grinder-viruses-intersect
#
