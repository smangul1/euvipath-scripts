#!/bin/sh
#$ -S /bin/bash
#$ -N job-mcp_nlapier2
#$ -cwd
#$ -o stdout-mcp.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=12:00:00

source ~/scratch/mcp-master/venv/bin/activate
python ~/scratch/mcp-master/mbprofile.py ~/scratch/mcp-master/test/out.m8 202
deactivate
