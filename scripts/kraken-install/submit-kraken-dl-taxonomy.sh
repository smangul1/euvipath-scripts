#!/bin/sh
#$ -S /bin/bash
#$ -N job-dl-kraken-taxo_nlapier2
#$ -cwd
#$ -o stdout-dl-kraken-taxo.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=2G,h_rt=2:00:00

source ~/.bash_profile

~/kraken-0.10.5-beta/kraken-build --download-taxonomy --db kraken_db_viruses #--db kraken_bvfpa_080416

