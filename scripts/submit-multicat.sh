#!/bin/sh
#$ -S /bin/bash
#$ -N job-multicat_nlapier2
#$ -cwd
#$ -o stdout-multicat.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=1G,h_rt=24:00:00

python ~/scratch/scripts/multicat.py ~/scratch/data/hmp/SRS011098/ ~/scratch/data/hmp/SRS013876/ ~/scratch/data/hmp/SRS019016/ ~/scratch/data/hmp/SRS019120/ ~/scratch/data/hmp/SRS052697/ ~/scratch/data/hmp/SRS011086/ ~/scratch/data/hmp/SRS011269/ ~/scratch/data/hmp/SRS014689/ ~/scratch/data/hmp/SRS019026/ ~/scratch/data/hmp/SRS045049/
