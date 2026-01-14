#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1
#SBATCH --cpus-per-task=30
#SBATCH --mem=120G
#SBATCH --time=48:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com
#SBATCH --job-name=extract_flanks_newest
#SBATCH --output=extract_flanks_newest_arrayjob%A_%a.o
#SBATCH --error=extract_flanks_newest_arrayjob%A_%a.e
#SBATCH --array=0-129

module load samtools

# Paths to BED and BAM directories
bed_dir="/home/alextu/scratch/SVcoords_sorted"
bam_dir="/home/alextu/scratch/primary_bams_hgsvc3_verkko123"
output_dir="/home/alextu/scratch/extract_sv_flanks_2000bp/extracted_flanks"

# Get all BAM files and sort them
bam_files=($(ls ${bam_dir}/*hap*.bam | sort))

# Debugging: Print the list of BAM files
echo "BAM files found: ${bam_files[@]}" >&2

# Get the BAM file for the current array task
bam_file="${bam_files[$SLURM_ARRAY_TASK_ID - 1]}"

# Debugging: Print the current BAM file being processed
echo "Processing BAM file: $bam_file" >&2

# Extract sample name and haplotype from BAM file (e.g., HG00171_hap1_primary.bam)
sample_haplotype=$(basename "$bam_file" | cut -d'_' -f1,2)

# Debugging: Print the extracted sample and haplotype
echo "Extracted sample and haplotype: $sample_haplotype" >&2

# Extract the sample name and haplotype separately
sample_name=$(echo "$sample_haplotype" | cut -d'_' -f1)  # e.g., HG00171
haplotype=$(echo "$sample_haplotype" | cut -d'_' -f2)    # e.g., hap1

# Map the haplotype to the corresponding BED file
if [[ "$haplotype" == "hap1" ]]; then
    bed_file="${bed_dir}/${sample_name}.h1.SVlength.SVcoords2000flank_bedtools.bed"
else
    bed_file="${bed_dir}/${sample_name}.h2.SVlength.SVcoords2000flank_bedtools.bed"
fi

# Output file for the current sample and haplotype
output_file="${output_dir}/${sample_name}_${haplotype}_SVflanks.csv"

# Add the header to the CSV file
echo "Region,SV Type,Flanking Sequence,Flank Length" > "$output_file"

# Temporary file for this task
temp_fasta="/home/alextu/scratch/extract_sv_flanks_2000bp/temp_${sample_name}_${haplotype}.fa"

# Index the BAM file if not already indexed
samtools index -b "$bam_file"

# Function to calculate the sequence length
get_seq_length() {
    grep -v "^>" "$temp_fasta" | tr -d '\n' | wc -c
}

# Function to read the sequence from the FASTA file
get_sequence() {
    grep -v "^>" "$temp_fasta" | tr -d '\n'
}

# Function to generate the consensus sequence using samtools
generate_consensus() {
    local region="$1"
    >&2 echo "Generating consensus for region: $region"
    samtools consensus -r "$region" --show-ins no -a "$bam_file" -o "$temp_fasta" --mode simple
}

# Function to extend flanks and ensure they are at least 2000bp long
ensure_flank_length() {
    local region="$1"
    local desired_length=2000
    local flank_type="$2"  # Pass the type of flank: "pre" or "post"
    
    generate_consensus "$region"
    local seq_length=$(get_seq_length)

    # Keep adjusting the region if the sequence is too short
    while [ "$seq_length" -lt "$desired_length" ]; do
        local chr=$(echo "$region" | cut -d':' -f1)
        local start=$(echo "$region" | cut -d':' -f2 | cut -d'-' -f1)
        local end=$(echo "$region" | cut -d':' -f2 | cut -d'-' -f2)

        local missing_bases=$((desired_length - seq_length))
        >&2 echo "Adjusting region. Current length: $seq_length, missing: $missing_bases"

        # Adjust start for pre-flank, and adjust end for post-flank
        if [[ "$flank_type" == "pre" ]]; then
            # Adjust the start (shrink toward 0 for pre-flanks)
            start=$((start - missing_bases))
            if [ "$start" -lt 0 ]; then
                >&2 echo "Start position is below 0, stopping extension"
                start=0  # Prevent negative start positions
                break
            fi
        else
            # Check if the end exceeds the chromosome length
            chrom_length=$(samtools view -H "$bam_file" | grep "^@SQ" | grep -w "$chr" | cut -f3 | cut -d':' -f2)
            if [ "$end" -ge "$chrom_length" ]; then
                >&2 echo "End position exceeds chromosome length ($chrom_length), stopping extension"
                break
            fi

            # Adjust the end (extend the end for post-flanks)
            end=$((end + missing_bases))
        fi

        # Update the region and regenerate the sequence
        region="${chr}:${start}-${end}"
        >&2 echo "New region: $region"
        generate_consensus "$region"
        seq_length=$(get_seq_length)
    done

    # Return the updated region
    echo "$region"
}

# Loop through the BED file and process each flank
while read -r chr pre_start pre_end sv_info rest_of_line; do
    # Read the next line for the post-flank
    read -r chr_next post_start post_end sv_info_next rest_of_line_next

    # Extract the SV info up to "INS" or "DEL"
    sv_type=$(echo "$sv_info" | grep -oP '.*?(INS|DEL)')
    sv_type_next=$(echo "$sv_info_next" | grep -oP '.*?(INS|DEL)')

    # Adjust the post-start for insertions by adding 1
    if [[ "$sv_type_next" == *"INS"* ]]; then
        post_start=$((post_start + 1))
    fi

    # Extract and adjust the pre-flank region
    pre_region="${chr}:${pre_start}-${pre_end}"
    >&2 echo "Pre-flank region: $pre_region"
    adjusted_pre_region=$(ensure_flank_length "$pre_region" "pre")
    pre_flank_seq=$(get_sequence)
    pre_flank_len=$(get_seq_length)

    # Check if the pre-flank length is 2001 for an insertion or deletion and adjust the start if necessary
    if [[ ("$sv_type" == *"INS"* || "$sv_type" == *"DEL"*) && "$pre_flank_len" -eq 2001 ]]; then
        pre_start=$((pre_start + 1))
        pre_region="${chr}:${pre_start}-${pre_end}"
        adjusted_pre_region=$(ensure_flank_length "$pre_region" "pre")
        pre_flank_seq=$(get_sequence)
        pre_flank_len=$(get_seq_length)
        >&2 echo "Pre-flank for $sv_type was 2001bp, adjusted start to $pre_start"
    fi

    # Extract and adjust the post-flank region
    post_region="${chr_next}:${post_start}-${post_end}"
    >&2 echo "Post-flank region: $post_region"
    adjusted_post_region=$(ensure_flank_length "$post_region" "post")
    post_flank_seq=$(get_sequence)
    post_flank_len=$(get_seq_length)

    # Check if the post-flank length is 2001 for a deletion and adjust the end if necessary
    if [[ "$sv_type_next" == *"DEL"* && "$post_flank_len" -eq 2001 ]]; then
        post_end=$((post_end - 1))
        post_region="${chr_next}:${post_start}-${post_end}"
        adjusted_post_region=$(ensure_flank_length "$post_region" "post")
        post_flank_seq=$(get_sequence)
        post_flank_len=$(get_seq_length)
        >&2 echo "Post-flank for deletion was 2001bp, adjusted end to $post_end"
    fi

    # Write the pre-flank and post-flank results to the output file, including the whole SV info and sequence length
    echo "${adjusted_pre_region},${sv_type},${pre_flank_seq},${pre_flank_len}" >> "$output_file"
    echo "${adjusted_post_region},${sv_type_next},${post_flank_seq},${post_flank_len}" >> "$output_file"

done < "$bed_file"

# Cleanup
rm "$temp_fasta"