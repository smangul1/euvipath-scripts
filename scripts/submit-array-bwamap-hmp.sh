#!/bin/sh
#$ -S /bin/bash
#$ -N job-array-bwamap-hmp_nlapier2
#$ -cwd
#$ -o stdout-array-bwamap-hmp.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=35G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa
source ~/.bash_profile

INDEXBASE='/u/home/n/nlapier2/scratch/data/bwa/'
READBASE='/u/home/n/nlapier2/scratch/data/'
#INDICES=(archaea-kraken.fa viral.fna fungi-kraken.fa protozoa.fa viruses_15062016.fa ref_intersect.fa vipr/NONFLU_All.fastq eupath/ameoba.fa eupath/crypto.fa eupath/fungi.fa eupath/giardia.fa eupath/microsporidia.fa eupath/piroplasma.fa eupath/plasmo.fa eupath/toxo.fa eupath/trich.fa eupath/tritryp.fa)
#READS=(hmp/SRS011086.fastq hmp/SRS011098.fastq hmp/SRS011269.fastq hmp/SRS013876.fastq hmp/SRS014689.fastq hmp/SRS019016.fastq hmp/SRS019026.fastq hmp/SRS019120.fastq hmp/SRS045049.fastq hmp/SRS052697.fastq hmp/SRS011086-paired.fastq hmp/SRS011098-paired.fastq hmp/SRS011269-paired.fastq hmp/SRS013876-paired.fastq hmp/SRS014689-paired.fastq hmp/SRS019016-paired.fastq hmp/SRS019026-paired.fastq hmp/SRS019120-paired.fastq hmp/SRS045049-paired.fastq hmp/SRS052697-paired.fastq hmp/SRS011086-singleton.fastq hmp/SRS011098-singleton.fastq hmp/SRS011269-singleton.fastq hmp/SRS013876-singleton.fastq hmp/SRS014689-singleton.fastq hmp/SRS019016-singleton.fastq hmp/SRS019026-singleton.fastq hmp/SRS019120-singleton.fastq hmp/SRS045049-singleton.fastq hmp/SRS052697-singleton.fastq)
INDICES=(archaea-kraken.fa vipr/NONFLU_All.fastq eukaryotes-notritryp.fa)
READS=(hmp/SRS011269.fastq hmp/SRS013876.fastq hmp/SRS019016.fastq hmp/SRS019120.fastq hmp/SRS045049.fastq)

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
