#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=32
#SBATCH --mem=100G # MEMORY PER NODE
#SBATCH --time=48:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=process_free_energies_chunks_array
#SBATCH --output=process_free_energies_chunks_array_%A_%a.o
#SBATCH --error=process_free_energies_chunks_array_%A_%a.e
#SBATCH --array=0-129


module load python/3.11
module load scipy-stack

python /home/alextu/projects/def-sushant/alextu/PhasedHapAssembly-nonB/IR_free_energy_scripts/whole_genome/process_free_energies_chunks_array_wholegenome.py $SLURM_ARRAY_TASK_ID
