#!/bin/sh
#$ -S /bin/bash
#$ -N job-array-bwamap-nyc_nlapier2
#$ -cwd
#$ -o stdout-array-bwamap-nyc.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=20G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa
source ~/.bash_profile

INDEXBASE='/u/home/n/nlapier2/scratch/data/bwa/'
READBASE='/u/home/n/nlapier2/scratch/data/'
#INDICES=(archaea-kraken.fa viral.fna fungi-kraken.fa protozoa.fa viruses_15062016.fa ref_intersect.fa vipr/NONFLU_All.fastq eukaryotes.fa eupath/amoeba.fa eupath/crypto.fa eupath/fungi.fa eupath/giardia.fa eupath/microsporidia.fa eupath/piroplasma.fa eupath/plasmo.fa eupath/toxo.fa eupath/trich.fa eupath/trityp.fa bacteria-kraken.fna)
INDICES=(archaea-kraken.fa vipr/NONFLU_All.fastq eukaryotes-notritryp.fa)
READS=(metasub/nycsub/SRR1748618.fastq metasub/nycsub/SRR1748620.fastq metasub/nycsub/SRR1748663.fastq metasub/nycsub/SRR1748670.fastq metasub/nycsub/SRR1748707.fastq metasub/nycsub/SRR1748708.fastq metasub/nycsub/SRR1749083.fastq metasub/nycsub/SRR1749599.fastq)

SGE_TASK_ID=$((${SGE_TASK_ID} - 1))
echo $SGE_TASK_ID
#echo $INDEXBASE${INDICES[$((${SGE_TASK_ID}%${#INDICES[@]}))]}
#echo $READBASE${READS[$((${SGE_TASK_ID}/${#INDICES[@]}))]}
IND=$INDEXBASE${INDICES[$((${SGE_TASK_ID}%${#INDICES[@]}))]}
REA=$READBASE${READS[$((${SGE_TASK_ID}/${#INDICES[@]}))]}

PAIRED=''
if [[ $REA == *"paired"* ]]; then
	PAIRED=' --paired'
fi

python /u/home/n/nlapier2/scratch/scripts/bwamap.py --index $IND --reads $REA$PAIRED
#
