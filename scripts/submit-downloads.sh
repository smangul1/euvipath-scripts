#!/bin/sh
#$ -S /bin/bash
#$ -N job-download_nlapier2
#$ -cwd
#$ -o stdout-download.out
#$ -M nathanl2012@gmail.com
#$ -m abe
#$ -l h_data=10G,h_rt=24:00:00

wget ftp://public-ftp.hmpdacc.org/Illumina/anterior_nares/SRS013876.tar.bz2
wget ftp://public-ftp.hmpdacc.org/Illumina/buccal_mucosa/SRS045049.tar.bz2
wget ftp://public-ftp.hmpdacc.org/Illumina/palatine_tonsils/SRS019026.tar.bz2
wget ftp://public-ftp.hmpdacc.org/Illumina/posterior_fornix/SRS011269.tar.bz2
wget ftp://public-ftp.hmpdacc.org/Illumina/right_retroauricular_crease/SRS019016.tar.bz2
wget ftp://public-ftp.hmpdacc.org/Illumina/saliva/SRS019120.tar.bz2
wget ftp://public-ftp.hmpdacc.org/Illumina/stool/SRS052697.tar.bz2
wget ftp://public-ftp.hmpdacc.org/Illumina/supragingival_plaque/SRS011098.tar.bz2
wget ftp://public-ftp.hmpdacc.org/Illumina/throat/SRS014689.tar.bz2
wget ftp://public-ftp.hmpdacc.org/Illumina/tongue_dorsum/SRS011086.tar.bz2
#
