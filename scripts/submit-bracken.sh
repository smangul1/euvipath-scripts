#!/bin/sh
#$ -S /bin/bash
#$ -N job-bracken_nlapier2
#$ -cwd
#$ -o stdout-bracken.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

python ~/scratch/Bracken-master/generate_kmer_distribution.py -i ~/scratch/results/virus-res/kraken-viruses-low-otus.txt -o bracken-viruses-low-kmer-distribution.txt
python ~/scratch/Bracken-master/est_abundance.py -i ~/scratch/results/virus-res/kraken-viruses-low-report.txt -k bracken-viruses-low-kmer-distribution.txt -o bracken-viruses-low-abundances.txt

