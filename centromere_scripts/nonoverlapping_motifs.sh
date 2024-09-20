#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G # MEMORY PER NODE
#SBATCH --time=10:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=nonoverlapping_motifs
#SBATCH --output=nonoverlapping_motifs.o
#SBATCH --error=nonoverlapping_motifs.e

module load python/3.10
module load scipy-stack
module load bedtools

python /home/alextu/scratch/centromere_analysis/centromere_scripts/nonoverlapping_motifs.py