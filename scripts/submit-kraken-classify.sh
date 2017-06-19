#!/bin/sh
#$ -S /bin/bash
#$ -N job-kraken-classify_nlapier2
#$ -cwd
#$ -o stdout-kraken-classify.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

#time ~/kraken-0.10.5-beta/kraken --db ~/scratch/Kraken_db_install_scripts-master/kraken_db_fungi/ ~/scratch/data/grinder/grinder-fungi-intersect-mutated-reads.fa > kraken-fungi-intersect-mutated-otus.txt

#~/kraken-0.10.5-beta/kraken-translate --db ~/scratch/Kraken_db_install_scripts-master/kraken_db_fungi/ kraken-fungi-intersect-mutated-otus.txt > kraken-fungi-intersect-mutated-results.kraken

time ~/kraken-0.10.5-beta/kraken --db ~/scratch/minikraken_20141208/ ~/scratch/data/grinder/grinder-viruses-intersect-mutated10-reads.fa > kraken-viruses-intersect-mutated10-otus.txt

~/kraken-0.10.5-beta/kraken-translate --db ~/scratch/minikraken_20141208/ kraken-viruses-intersect-mutated10-otus.txt > kraken-viruses-intersect-mutated10-results.kraken

