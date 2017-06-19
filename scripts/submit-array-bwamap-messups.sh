#!/bin/sh
#$ -S /bin/bash
#$ -N job-array-bwamap-messups_nlapier2
#$ -cwd
#$ -o stdout-array-bwamap-messups.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=30G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa
source ~/.bash_profile

INDEXBASE='/u/home/n/nlapier2/scratch/data/bwa/'
READBASE='/u/home/n/nlapier2/scratch/data/'
INDICES=(eukaryotes-notritryp.fa)
READS=(metasub/sacramento/Sample_1A.fastq metasub/sacramento/Sample_1B.fastq metasub/sacramento/Sample_1C.fastq metasub/sacramento/Sample_2A.fastq metasub/sacramento/Sample_2B.fastq metasub/sacramento/Sample_2C.fastq hmp/SRS011086-singleton.fastq hmp/SRS011098-singleton.fastq hmp/SRS011269-singleton.fastq hmp/SRS013876-singleton.fastq hmp/SRS014689-singleton.fastq hmp/SRS019016-singleton.fastq hmp/SRS019120-singleton.fastq hmp/SRS045049-singleton.fastq hmp/SRS052697-singleton.fastq)

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
