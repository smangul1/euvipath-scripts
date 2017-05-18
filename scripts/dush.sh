#!/bin/sh
#$ -S /bin/bash
#$ -N job_dush_nlapier2
#$ -cwd
#$ -o stdout-dush.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=12:00:00

du -sh . 

