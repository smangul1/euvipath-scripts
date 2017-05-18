#!/bin/sh
#$ -S /bin/bash
#$ -N job-kraken-classify_nlapier2
#$ -cwd
#$ -o stdout-kraken-classify.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

time ~/kraken-0.10.5-beta/kraken --db ~/scratch/minikraken_20141208 ~/scratch/kraken-data/timing/simBA5_timing.fa > kraken-simba-timing-otus.txt

~/kraken-0.10.5-beta/kraken-translate --db ~/scratch/minikraken_20141208 kraken-simba-timing-otus.txt > kraken-simba-timing-results.kraken
