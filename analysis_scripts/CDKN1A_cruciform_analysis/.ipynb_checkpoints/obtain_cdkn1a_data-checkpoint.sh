#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G # MEMORY PER NODE
#SBATCH --time=1:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=obtain_cdkn1a_data
#SBATCH --output=obtain_cdkn1a_data.o
#SBATCH --error=obtain_cdkn1a_data.e

module load python/3.11
module load scipy-stack

python /home/alextu/projects/def-sushant/alextu/PhasedHapAssembly-nonB/analysis_scripts/obtain_cdkn1a_data.py