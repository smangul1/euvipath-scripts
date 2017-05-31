#!/bin/sh
#$ -S /bin/bash
#$ -N job-fastq-convert_nlapier2
#$ -cwd
#$ -o stdout-fastq-convert.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

source ~/.bash_profile

for fastq in ~/scratch/nycsub/*
do
	fastq_to_fasta -Q33 -i $fastq -o ${fastq%?}a
done


