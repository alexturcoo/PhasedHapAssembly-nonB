#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=150G
#SBATCH --time=48:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com
#SBATCH --output=find_nonb_motifs_hap1_%A_%a.o
#SBATCH --error=find_nonb_motifs_hap1_%A_%a.e
#SBATCH --array=0-3   # Modify this based on the number of samples

# Directory containing input FASTA files
INPUT_DIR="/home/alextu/scratch/haplotigs_fastas_hgsvc_verkko123/all_fastas"

# Output directory for non-B DNA annotations
OUTPUT_DIR="/home/alextu/scratch/nonb_motif_annotations_hgsvc/verkko_123_haplotigs/"

# Get list of input files
files=("$INPUT_DIR"/*.fasta)

# Get the input file corresponding to the current array task ID
input_file="${files[$SLURM_ARRAY_TASK_ID - 1]}"
echo $input_file

if [ -f "$input_file" ]; then
    # Extract filename without extension
    filename=$(basename "$input_file")
    filename_no_ext="${filename%.*}"
    echo $filename
    echo $filename_no_ext

    # Create output directory based on the sample name
    output_subdir="${OUTPUT_DIR}${filename_no_ext}/"
    mkdir -p "$output_subdir"

    # Run the gfa tool on the selected input file
    ./gfa -skipWGET \
         -seq "$input_file" \
         -out $filename_no_ext
else
    echo "Error: Input file not found for task $SLURM_ARRAY_TASK_ID"
fi
