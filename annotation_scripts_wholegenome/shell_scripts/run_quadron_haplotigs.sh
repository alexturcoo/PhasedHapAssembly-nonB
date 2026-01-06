#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=80G
#SBATCH --time=15:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com
#SBATCH --output=run_quadron_%A_%a.o
#SBATCH --error=run_quadron_%A_%a.e
#SBATCH --array=0-19  # Modify this based on the number of files

module load gcc r
module load openmpi

# Base directory containing all FASTA files
BASE_DIR="/home/alextu/scratch/haplotigs_fastas_hgsvc_verkko123/all_fastas_split"

# Output directory
OUTPUT_DIR="/home/alextu/scratch/nonb_motif_annotations_hgsvc/verkko_123_haplotigs/quadron_annotations"

# Get list of FASTA files
files=("$BASE_DIR"/HG00171*.fasta)

# Get the total number of files
total_files=${#files[@]}

# Check if the current task ID is within the range of available files
if [ $SLURM_ARRAY_TASK_ID -lt $total_files ]; then
    # Get the current FASTA file based on the task ID
    FASTA_FILE="${files[$SLURM_ARRAY_TASK_ID]}"
    echo "Processing $FASTA_FILE"
    BASENAME=$(basename "$FASTA_FILE" .fasta)
    OUTPUT_FILE="${OUTPUT_DIR}/${BASENAME}_verkko_batch123.txt"

    # Run the R script with the current FASTA file
    Rscript -e "
        print('NOTE: Loading Quadron core...', quote=FALSE);
        load('Quadron.lib');
        Quadron(
            FastaFile = '$FASTA_FILE',
            OutFile = '$OUTPUT_FILE',
            nCPU = 12,
            SeqPartitionBy = 1000
        )
    "

    echo "Processing complete for $FASTA_FILE. Results are saved in $OUTPUT_FILE."
else
    echo "Error: Task ID $SLURM_ARRAY_TASK_ID is out of range for available files."
fi
