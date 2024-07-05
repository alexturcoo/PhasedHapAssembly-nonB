#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G # MEMORY PER NODE
#SBATCH --time=3:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=process_gquad_beds
#SBATCH --output=process_gquad_beds.o
#SBATCH --error=process_gquad_beds.e

module load python/3.10
module load scipy-stack
module load bedtools

python /home/alextu/scratch/phased_haplotype_verkko_alignments_workflow/process_gquad_beds_quadron.py