#!/bin/sh
#$ -S /bin/bash
#$ -N job-rm_nlapier2
#$ -cwd
#$ -o stdout-rm.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=1G,h_rt=24:00:00

rm -r ~/scratch/mcp-master/venv/
