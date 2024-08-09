#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=1
#SBATCH --mem=40G # MEMORY PER NODE
#SBATCH --time=1:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=process_quadron_files
#SBATCH --output=process_quadron_files.o
#SBATCH --error=process_quadron_files.e

module load python/3.10
module load scipy-stack
module load bedtools

python /home/alextu/scratch/rdna_analysis/rdna_scripts/process_quadron_files_rdna.py