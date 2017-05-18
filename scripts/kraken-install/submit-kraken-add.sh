#!/bin/sh
#$ -S /bin/bash
#$ -N job-kraken-add_nlapier2
#$ -cwd
#$ -o stdout-kraken-add.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

source ~/.bash_profile

for dir in fungi protozoa archaea viral bacteria; do
        for fna in `ls $dir/*.fna`; do
                ~/kraken-0.10.5-beta/kraken-build --add-to-library $fna --db kraken_bvfpa_080416
        done
done


