#!/bin/sh
#$ -S /bin/bash
#$ -N job-array-bwamap-bacteria_nlapier2
#$ -cwd
#$ -o stdout-array-bwamap-bacteria.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=55G,highp,h_rt=48:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa
source ~/.bash_profile

INDEXBASE='/u/home/n/nlapier2/scratch/data/bwa/'
READBASE='/u/home/n/nlapier2/scratch/data/'
INDICES=(bacteria-kraken.fna)
READS=(metasub/nycsub/SRR1748618.fastq metasub/nycsub/SRR1748620.fastq metasub/nycsub/SRR1748663.fastq metasub/nycsub/SRR1748670.fastq metasub/nycsub/SRR1748707.fastq metasub/nycsub/SRR1748708.fastq metasub/nycsub/SRR1749083.fastq metasub/nycsub/SRR1749599.fastq)
#READS=(metasub/sacramento/Sample_1A.fastq metasub/sacramento/Sample_1B.fastq metasub/sacramento/Sample_1C.fastq metasub/sacramento/Sample_2A.fastq metasub/sacramento/Sample_2B.fastq metasub/sacramento/Sample_2C.fastq hmp/SRS011086.fastq hmp/SRS011098.fastq hmp/SRS011269.fastq hmp/SRS013876.fastq hmp/SRS014689.fastq hmp/SRS019016.fastq hmp/SRS019026.fastq hmp/SRS019120.fastq hmp/SRS045049.fastq hmp/SRS052697.fastq hmp/SRS011086-paired.fastq hmp/SRS011098-paired.fastq hmp/SRS011269-paired.fastq hmp/SRS013876-paired.fastq hmp/SRS014689-paired.fastq hmp/SRS019016-paired.fastq hmp/SRS019026-paired.fastq hmp/SRS019120-paired.fastq hmp/SRS045049-paired.fastq hmp/SRS052697-paired.fastq hmp/SRS011086-singleton.fastq hmp/SRS011098-singleton.fastq hmp/SRS011269-singleton.fastq hmp/SRS013876-singleton.fastq hmp/SRS014689-singleton.fastq hmp/SRS019016-singleton.fastq hmp/SRS019026-singleton.fastq hmp/SRS019120-singleton.fastq hmp/SRS045049-singleton.fastq hmp/SRS052697-singleton.fastq)

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
