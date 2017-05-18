#!/bin/sh
#$ -S /bin/bash
#$ -N job_chunk_nlapier2
#$ -cwd
#$ -o stdout-chunk.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

python remove-chunk.py 268400000 268400000

