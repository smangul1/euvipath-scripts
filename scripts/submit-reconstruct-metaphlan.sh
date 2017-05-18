#!/bin/sh
#$ -S /bin/bash
#$ -N job-reconstruct-metaphlan_nlapier2
#$ -cwd
#$ -o stdout-reconstruct-metaphlan.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bowtie2
source ~/.bash_profile

bowtie2-inspect ~/metaphlan2/db_v20/mpa_v20_m200 > ~/markers.fasta

