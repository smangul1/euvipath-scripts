#!/bin/sh
#$ -S /bin/bash
#$ -N job-array-domain-quantify_nlapier2
#$ -cwd
#$ -o stdout-array-domain-quantify.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

. /u/local/Modules/default/init/modules.sh
module load bwa
source ~/.bash_profile

#SAMPLES=(Sample_1A Sample_1B Sample_1C Sample_2A Sample_2B Sample_2C)
#SAMPLES=(SRS011269 SRS013876 SRS019016 SRS019120 SRS045049)
SAMPLES=(SRR1748618 SRR1748620 SRR1748663 SRR1748670 SRR1748707 SRR1748708 SRR1749083 SRR1749599)

#SGE_TASK_ID=$1
SGE_TASK_ID=$((${SGE_TASK_ID} - 1))
echo $SGE_TASK_ID
SMP=${SAMPLES[${SGE_TASK_ID}]}

#echo 'time python ~/scratch/scripts/domain-quantify.py ~/scratch/data/metasub/sacramento/'${SMP}'.fastq results/hmp-sacramento-nyc/ '$SMP
#time python ~/scratch/scripts/domain-quantify.py ~/scratch/data/metasub/sacramento/${SMP}.fastq ~/scratch/results/hmp-sacramento-nyc/ $SMP > ${SMP}.out
#time python ~/scratch/scripts/domain-quantify.py ~/scratch/data/hmp/${SMP}.fastq ~/scratch/results/hmp-sacramento-nyc/ $SMP > ${SMP}.out
time python ~/scratch/scripts/domain-quantify.py ~/scratch/data/metasub/nycsub/${SMP}.fastq ~/scratch/results/hmp-sacramento-nyc/ $SMP > ${SMP}.out
#
