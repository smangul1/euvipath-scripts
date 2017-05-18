#!/bin/sh
#$ -S /bin/bash
#$ -N job-kraken-report_nlapier2
#$ -cwd
#$ -o stdout-kraken-report.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

~/kraken-0.10.5-beta/kraken-report --db ~/scratch/minikraken_20141208 ~/scratch/results/virus-res/kraken-viruses-low-otus.txt

