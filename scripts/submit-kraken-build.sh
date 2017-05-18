#!/bin/sh
#$ -S /bin/bash
#$ -N job-kraken-build_nlapier2
#$ -cwd
#$ -o stdout-kraken-build.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=50G,h_rt=14:00:00

source ~/.bash_profile

~/kraken-0.10.5-beta/kraken-build --standard --threads 16 --db kraken-full-db --jellyfish-hash-size 6400M

