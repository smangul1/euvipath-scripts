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

#time ~/metaphlan2/metaphlan2.py ~/scratch/data/nycsub/SRR1749083.fasta --bowtie2out bowtie2-nycsub-anthrax-SRR1749083.bz2 --nproc 20 --input_type fasta > metaphlan-nycsub-anthrax-SRR1749083-profile.txt

#time ~/metaphlan2/metaphlan2.py ~/scratch/data/nycsub/SRR1749599.fasta --bowtie2out bowtie2-nycsub-plague-SRR1749599.bz2 --nproc 20 --input_type fasta > metaphlan-nycsub-plague-SRR1749599-profile.txt

time ~/metaphlan2/metaphlan2.py ~/scratch/data/grinder/grinder-viruses-intersect-reads.fa --bowtie2out bowtie2-viruses-intersect.bz2 --nproc 20 --input_type fasta > metaphlan-viruses-intersect-profile.txt
#
