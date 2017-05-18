#!/bin/sh
#$ -S /bin/bash
#$ -N job-kraken-build_nlapier2
#$ -cwd
#$ -o stdout-kraken-build.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=124G,h_rt=12:00:00

source ~/.bash_profile

~/kraken-0.10.5-beta/kraken-build --build --db kraken_bvfpa_080416 --jellyfish-hash-size 6400M

