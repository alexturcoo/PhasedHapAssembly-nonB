#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --time=3:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com
#SBATCH --output=extract_rdna_verkko_%A_%a.o
#SBATCH --error=extract_rdna_verkko_%A_%a.e
#SBATCH --array=0-64   # Modify based on the number of BAM files

module load python/3.10
module load scipy-stack
module load bedtools

python /home/alextu/scratch/rdna_analysis/rdna_scripts/extract_rdna_verkko123_chm13_alignments.py $SLURM_ARRAY_TASK_ID