#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=1
#SBATCH --mem=120G # MEMORY PER NODE
#SBATCH --time=3:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=bedtools_intersect
#SBATCH --output=bedtools_intersect.o
#SBATCH --error=bedtools_intersect.e

module load bedtools

# Variables
REFERENCE_BED="/home/alextu/scratch/results/bed_files/chm13_ref_genome/chm13v2.0_nonb_annotations_collapsed/IR/IR.collapsed.bed"
BED_DIR="/home/alextu/scratch/results/bed_files/all_IR_beds_verkko_batch123_collapsed_chm13"
OUTPUT_DIR="/home/alextu/scratch/results"
OVERLAPPING_OUTPUT="$OUTPUT_DIR/verkko_batch123_chm13_IR_intersected_output.bed"
NON_OVERLAPPING_OUTPUT="$OUTPUT_DIR/verkko_batch123_chm13_IR_nonoverlapping_output.bed"
FINAL_OUTPUT="$OUTPUT_DIR/verkko_batch123_chm13_IR_final_output.bed"

# Create a list of BED files
BED_FILES=($BED_DIR/*collapsed.bed)

# Process each BED file: remove everything up to and including the | in the first column and sort the file
for file in "${BED_FILES[@]}"; do
    awk -F'|' '{print $2}' "$file" | sort -k1,1 -k2,2n -k3,3n > "${file}.processed"
done

# Update BED_FILES to point to the processed files
BED_FILES=(${BED_FILES[@]/%/.processed})

# Extract file names to use as labels
NAMES=($(for file in ${BED_FILES[@]}; do basename "$file" .processed; done))

# Convert the array of names to a space-separated string
NAMES_STR=$(IFS=' ' ; echo "${NAMES[*]}")

# Run bedtools intersect with -names option for overlapping motifs
bedtools intersect -wa -wb \
    -a <(sort -k1,1 -k2,2n -k3,3n $REFERENCE_BED) \
    -b ${BED_FILES[@]} \
    -names $NAMES_STR \
    -sorted > $OVERLAPPING_OUTPUT

# Run bedtools intersect with -v option for non-overlapping motifs
#bedtools intersect -v \
#    -a <(sort -k1,1 -k2,2n -k3,3n $REFERENCE_BED) \
#    -b ${BED_FILES[@]} > $NON_OVERLAPPING_OUTPUT

# Combine overlapping and non-overlapping results
#cat $OVERLAPPING_OUTPUT $NON_OVERLAPPING_OUTPUT > $FINAL_OUTPUT

echo "Analysis complete. Overlapping results in $OVERLAPPING_OUTPUT" #, non-overlapping results in $NON_OVERLAPPING_OUTPUT, and combined results in $FINAL_OUTPUT"




