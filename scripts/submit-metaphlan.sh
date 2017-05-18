#!/bin/sh
#$ -S /bin/bash
#$ -N job-metaphlan_nlapier2
#$ -cwd
#$ -o stdout-metaphlan.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bowtie2
source ~/.bash_profile

#~/metaphlan2/metaphlan2.py ~/scratch/data/grinder/grinder-fungi-low-reads.fa --bowtie2out fungi-low-bowtie2.bz2 --nproc 20 --input_type fasta --tax_lev 's' > metaphlan-fungi-low-profile.txt

time ~/metaphlan2/metaphlan2.py ~/scratch/kraken-data/timing/simBA5_timing.fa --bowtie2out bowtie2-simba-timing.bz2 --nproc 20 --input_type fasta > metaphlan-simba-timing-profile.txt
#
