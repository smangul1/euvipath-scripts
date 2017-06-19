#!/bin/sh
#$ -S /bin/bash
#$ -N job-array-bwamap_nlapier2
#$ -cwd
#$ -o stdout-array-bwamap.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=55G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa
source ~/.bash_profile

INDEXBASE='/u/home/n/nlapier2/scratch/data/bwa/'
READBASE='/u/home/n/nlapier2/scratch/data/'
INDICES=(bacteria-kraken.fa archaea-kraken.fa viral.fna fungi-kraken.fa protozoa.fa viruses_15062016.fa ref_intersect.fa vipr/NONFLU_All.fastq eukaryotes.fa eukaryotes-notritryp.fa eupath/amoeba.fa eupath/crypto.fa eupath/fungi.fa eupath/giardia.fa eupath/microsporidia.fa eupath/piroplasma.fa eupath/plasmo.fa eupath/toxo.fa eupath/trich.fa eupath/trityp.fa)
READS=(metasub/sacramento/Sample_1A.fastq metasub/sacramento/Sample_1B.fastq metasub/sacramento/Sample_1C.fastq metasub/sacramento/Sample_2A.fastq metasub/sacramento/Sample_2B.fastq metasub/sacramento/Sample_2C.fastq hmp/SRS011086.fastq hmp/SRS011098.fastq hmp/SRS011269.fastq hmp/SRS013876.fastq hmp/SRS014689.fastq hmp/SRS019016.fastq hmp/SRS019026.fastq hmp/SRS019120.fastq hmp/SRS045049.fastq hmp/SRS052697.fastq hmp/SRS011086-paired.fastq hmp/SRS011098-paired.fastq hmp/SRS011269-paired.fastq hmp/SRS013876-paired.fastq hmp/SRS014689-paired.fastq hmp/SRS019016-paired.fastq hmp/SRS019026-paired.fastq hmp/SRS019120-paired.fastq hmp/SRS045049-paired.fastq hmp/SRS052697-paired.fastq hmp/SRS011086-singleton.fastq hmp/SRS011098-singleton.fastq hmp/SRS011269-singleton.fastq hmp/SRS013876-singleton.fastq hmp/SRS014689-singleton.fastq hmp/SRS019016-singleton.fastq hmp/SRS019026-singleton.fastq hmp/SRS019120-singleton.fastq hmp/SRS045049-singleton.fastq hmp/SRS052697-singleton.fastq)

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
