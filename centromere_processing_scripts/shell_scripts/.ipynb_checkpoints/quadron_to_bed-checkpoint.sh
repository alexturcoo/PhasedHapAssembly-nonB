#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G # MEMORY PER NODE
#SBATCH --time=10:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=quadron_to_bed
#SBATCH --output=quadron_to_bed.o
#SBATCH --error=quadron_to_bed.e

module load python/3.10
module load scipy-stack
module load bedtools

python /home/alextu/scratch/centromere_analysis/centromere_scripts/quadron_to_bed.py