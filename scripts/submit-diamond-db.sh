#!/bin/sh
#$ -S /bin/bash
#$ -N job-diamond-db_nlapier2
#$ -cwd
#$ -o stdout-dmnd-db.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

~/scratch/scripts/diamond makedb --in ~/scratch/data/viruses_15062016.aa -d viruses-aa.dmnd

