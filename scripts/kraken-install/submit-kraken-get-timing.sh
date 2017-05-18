#!/bin/sh
#$ -S /bin/bash
#$ -N job-kraken-timing_nlapier2
#$ -cwd
#$ -o stdout-kraken-timing.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

wget http://ccb.jhu.edu/software/kraken/dl/timing.tgz

