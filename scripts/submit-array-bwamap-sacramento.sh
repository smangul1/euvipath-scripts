#!/bin/sh
#$ -S /bin/bash
#$ -N job-array-bwamap-sacramento_nlapier2
#$ -cwd
#$ -o stdout-array-bwamap-sacramento.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=25G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa
source ~/.bash_profile

INDEXBASE='/u/home/n/nlapier2/scratch/data/bwa/'
READBASE='/u/home/n/nlapier2/scratch/data/'
#INDICES=(archaea-kraken.fa viral.fna fungi-kraken.fa protozoa.fa viruses_15062016.fa ref_intersect.fa vipr/NONFLU_All.fastq eukaryotes.fa eupath/amoeba.fa eupath/crypto.fa eupath/fungi.fa eupath/giardia.fa eupath/microsporidia.fa eupath/piroplasma.fa eupath/plasmo.fa eupath/toxo.fa eupath/trich.fa eupath/trityp.fa bacteria-kraken.fna)
INDICES=(archaea-kraken.fa vipr/NONFLU_All.fastq eukaryotes-notritryp.fa)
READS=(metasub/sacramento/Sample_1A.fastq metasub/sacramento/Sample_1B.fastq metasub/sacramento/Sample_1C.fastq metasub/sacramento/Sample_2A.fastq metasub/sacramento/Sample_2B.fastq metasub/sacramento/Sample_2C.fastq)

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
