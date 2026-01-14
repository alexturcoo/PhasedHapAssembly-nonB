#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 # specify number of gpus
#SBATCH --cpus-per-task=1
#SBATCH --mem=48G # MEMORY PER NODE
#SBATCH --time=20:00:00 # hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com # sends me an email once done
#SBATCH --job-name=extract_haplotype_centromeres
#SBATCH --output=extract_haplotype_centromeres.o
#SBATCH --error=extract_haplotype_centromeres.e

# This script extracts complete and accurately assembled chromosomes from full haplotype fasta files (not alignment based fastas).

module load StdEnv/2020 seqtk

# Define the directories
BED_DIR="/home/alextu/scratch/centromere_analysis/CEN_COORD_UPDATED_Aug7_logsdon/haplotype_level_beds_complete_and_accurate_active_asat_HOR_arrays"
FASTA_DIR="/path/to/fully/assembled/fastas"
OUTPUT_DIR="/home/alextu/scratch/centromere_analysis/haplotype_centromere_fastas_active_asat_HOR_arrays"

mkdir -p "$OUTPUT_DIR"

# Loop through each BED file in the directory
for BED_FILE in "$BED_DIR"/*.bed; do
    # Extract the sample name and haplotype from the BED file name
    FILENAME=$(basename "$BED_FILE" .bed)
    SAMPLE=$(echo "$FILENAME" | cut -d'_' -f1)
    HAPLOTYPE=$(echo "$FILENAME" | grep -oP 'haplotype[0-9]+' | sed 's/haplotype/hap/')

    # Construct the corresponding FASTA file path
    FASTA_FILE="$FASTA_DIR/$SAMPLE.vrk-ps-sseq.asm-$HAPLOTYPE.fasta"

    if [ ! -f "$FASTA_FILE" ]; then
        echo "FASTA file $FASTA_FILE not found, skipping $BED_FILE"
        continue
    fi

    # Extract the chromosome name from the BED file
    CHR=$(awk 'NR==1 {print $5}' "$BED_FILE")

    # Extract the sequence from the FASTA file using seqtk and save with the modified name
    seqtk subseq "$FASTA_FILE" "$BED_FILE" > "$OUTPUT_DIR/${FILENAME}_${CHR}.fasta"
done
