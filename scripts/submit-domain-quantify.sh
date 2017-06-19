#!/bin/sh
#$ -S /bin/bash
#$ -N job-domain-quantify_nlapier2
#$ -cwd
#$ -o stdout-domain-quantify.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa
source ~/.bash_profile

time python ~/scratch/scripts/domain-quantify.py ~/scratch/data/metasub/nycsub/SRR1748618.fastq ~/scratch/results/hmp-sacramento-nyc/ SRR1748618 > SRR1748618.out
#
