#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 # specify number of gpus
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G # MEMORY PER NODE
#SBATCH --time=1:00:00 # hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com # sends me an email once done
#SBATCH --job-name=create_centromere_bed
#SBATCH --output=create_centromere_bed.o
#SBATCH --error=create_centromere_bed.e

module load python/3.10
module load scipy-stack
module load bedtools

python /home/alextu/scratch/centromere_analysis/centromere_scripts/create_centromere_bed.py