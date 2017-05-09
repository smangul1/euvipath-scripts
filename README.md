# euvipath-scripts


Here we provide scripts and commands we used in our study "" to run existing microbiome profiling tools on both simulated and real data. Preprint of the study is available at 

# Compare to existing tools

We have compared euViPath to the following microbiome profiling tools:
* MetaPhlAn2, which version, https://bitbucket.org/biobakery/metaphlan2
* SURPI, v, http://chiulab.ucsf.edu/surpi/
* Kraken, v, https://ccb.jhu.edu/software/kraken/


# Datasets

We have performed profiling of eukaryotic and viral pathogens via euvipath across 3 studies.

### HMP

We have download 500 samples across 5 human tissues
### GTEx
We have downlaod 8555 samples across 53 human tissues
## Blood samples
The blood DNA virome in 8,000 humans
http://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1006292#ppat.1006292.s001
### Uran Microbiome
We haeve download x samples accross urban habitat


# How to run microbime profiling tools 

## SURPI
To install the tools we run 

To run the tool:

```
```

## Metahplan2
Source directory: /u/home/n/nlapier2/metaphlan2

Run metaphlan classify: /u/home/n/nlapier2/metaphlan2/metaphlan2.py reads.fa --bowtie2out bowtie2-output.bz2 --nproc 20 --input\_type fasta > metaphlan-profile.txt

## Kraken
Source directory: /u/home/n/nlapier2/kraken-0.10.5-beta

Minikraken DB (4GB): /u/home/n/nlapier2/scratch/minikraken\_20141208

Full Kraken DB (354GB): /u/home/n/nlapier2/scratch/kraken\_bvfpa\_080416

Run Kraken Classify: /u/home/n/nlapier2/kraken-0.10.5-beta/kraken --db $DBNAME seqs.fa


# How to run alignment tools

## Diamond
Source directory: /u/home/n/nlapier2/diamond-master

Create diamond-format database: /u/home/n/nlapier2/diamond-master/diamond --in reference.fa -d reference-db.dmnd

Run diamond alignment: /u/home/n/nlapier2/diamond-master/diamond blastx -d reference-db.dmnd -q reads.fa -o alignments.m8

You may have issues using the diamond executable; in this case, use diamond-sse2, which is in the same source directory

## BWA
Load BWA Module: . /u/local/Modules/default/init/modules.sh; module load bwa

Index the reference: bwa index reference.fa

This creates 5 files: reference.fa.amb reference.fa.ann reference.fa.bwt reference.fa.pac reference.fa.sa

The index base name is then reference.fa, but if you move it to the folder "bwa", then the index base name is bwa/reference.fa

Align: bwa mem {Index Base Name} reads.fa > bwa-viruses.sam


# Dealing with multimapped reads by BWA

Method 1: Discard multimapped reads; only keep uniquely-mapped reads

Method 2: Randomly pick a genome to assign the read to

Method 3: Let BWA choose which genome to map to

Results forthcoming...


# K-mer method for improved runtime

Precomputation: count k-mers in reference using Jellyfish

Count k-mers present in each read

Find which genomes the reads could possibly come from (no false negatives, probaably some false positives, look for at least one k-mer match)

Then for BWA only align the reads to the genomes that they could possibly come from

Determine which k-mer size produces the best speed
