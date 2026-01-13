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
#SBATCH --array=0-129  # Modify this based on the number of directories

### This script takes fasta files and runs the quadron tool (G4 detection) using an array job for each sample

module load gcc r
module load openmpi

# Base directory containing the subdirectories of FASTA files
BASE_DIR="/path/to/fasta/files/directory"

# Output directory
OUTPUT_DIR="/path/to/quadron/annotations"

# Get list of directories
directories=("$BASE_DIR"/HG* "$BASE_DIR"/NA*)

# Get the directory corresponding to the current array task ID
dir="${directories[$SLURM_ARRAY_TASK_ID]}"
echo "Processing directory: $dir"

if [ -d "$dir" ]; then
    # Create a corresponding output directory for the current input directory
    output_subdir="${OUTPUT_DIR}/$(basename "$dir")"
    mkdir -p "$output_subdir"

    # Iterate over each FASTA file in the directory
    for FASTA_FILE in "$dir"/*.fasta; do
        echo "Processing $FASTA_FILE"
        BASENAME=$(basename "$FASTA_FILE" .fasta)
        OUTPUT_FILE="${output_subdir}/${BASENAME}_verkko_batch3.txt"

        # Run the R script with the current FASTA file
        Rscript -e "
            print('NOTE: Loading Quadron core...', quote=FALSE);
            load('Quadron.lib');
            Quadron(
                FastaFile = '$FASTA_FILE',
                OutFile = '$OUTPUT_FILE',
                nCPU = 12,
                SeqPartitionBy = 1000000
            )
        "
    done

    echo "Processing complete for directory $dir. Results are saved in $output_subdir."
else
    echo "Error: Directory not found for task $SLURM_ARRAY_TASK_ID"
fi