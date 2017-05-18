#!/bin/sh
#$ -S /bin/bash
#$ -N job-bwa-index_nlapier2
#$ -cwd
#$ -o stdout-bwa-index.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=50G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa

bwa index ~/scratch/Kraken_db_install_scripts-master/all-kraken.fna

