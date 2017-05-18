#!/bin/sh
#$ -S /bin/bash
#$ -N job_translate_nlapier2
#$ -cwd
#$ -o stdout-translate.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

#echo $SGE_TASK_ID
#python translate.py $SGE_TASK_ID
python translate.py

