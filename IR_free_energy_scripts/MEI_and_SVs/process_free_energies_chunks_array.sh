#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=32
#SBATCH --mem=150G # MEMORY PER NODE
#SBATCH --time=2:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=create_density_plots
#SBATCH --output=create_density_plots.o
#SBATCH --error=create_density_plots.e
#SBATCH --array=0-129


module load python/3.11
module load scipy-stack

python /home/alextu/scratch/process_free_energies_chunks_array.py $SLURM_ARRAY_TASK_ID
