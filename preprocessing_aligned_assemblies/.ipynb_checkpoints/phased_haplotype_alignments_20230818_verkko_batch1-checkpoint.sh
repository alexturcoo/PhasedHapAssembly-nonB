#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G # MEMORY PER NODE
#SBATCH --time=24:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=run_phased_hap_alignment_fasta
#SBATCH --output=run_phased_hap_alignment_fasta.o
#SBATCH --error=run_phased_hap_alignment_fasta.e


### THIS SCRIPT TAKES PHASED HAPLOTYPE ASSEMBLY ALIGNMENTS FROM HGSVC3 VERKKO ALIGNED ASSEMBLIES BATCH 1,2,3
### CONVERTS THE ALIGNMENTS INTO FASTA FILES WITH CHROMOSOME ANNOTATION FOR DOWNSTREAM ANALYSIS
### Output will give you filtered BAM files as well as haplotype level FASTA FILES for non-B Annotation

module load samtools
module load bamtools

# Set the base directory containing subdirectories for each sample type
base_dir="/path/to/samples/folder/"

# Specify the output base directory for filtered BAM files
bam_output_base="/path/to/bam/outputfolder/"

# Specify the output base directory for FASTA files
fasta_output_base="/path/to/fasta/outputfolder/"

# Loop over subdirectories (each corresponding to a sample type)
for sample_dir in "${base_dir}"/*/; do
    if [[ -d "${sample_dir}" ]]; then
        # Extract the sample name (e.g., HG00268) from the subdirectory path
        sample_name=$(basename "${sample_dir}")

        # Create output directory for filtered BAM files based on sample name
        filtered_bam_output_dir="${bam_output_base}/${sample_name}"
        mkdir -p "${filtered_bam_output_dir}"

        # Loop over haplotypes (1 and 2)
        for hap in 1 2; do
            # Construct the input BAM file path for the current sample type and haplotype
            input_bam="${sample_dir}/${sample_name}.vrk-ps-sseq.asm-hap${hap}.hg38.sort.bam"

            # Construct the output primary BAM file path for the current sample type and haplotype
            output_primary_bam="${filtered_bam_output_dir}/${sample_name}_hap${hap}_primary.bam"

            # Filter BAM by alignment quality and save the filtered primary BAM file
            samtools view -b -F 256 -q 0 "${input_bam}" > "${output_primary_bam}"

            echo "Filtered and saved ${input_bam} to ${output_primary_bam}"

            # Split filtered primary BAM by chromosome
            bamtools split -in "${output_primary_bam}" -reference

            # Move output BAM files (by chromosome) to the desired output directory
            mv *REF_chr*.bam "${filtered_bam_output_dir}/"

            echo "Split BAM by chromosome for ${output_primary_bam}"

            # Create output directory for FASTA files based on sample name
            fasta_output_dir="${fasta_output_base}/${sample_name}"
            mkdir -p "${fasta_output_dir}"

            # Loop over split BAM files (by chromosome) and convert to FASTA
            for bam_chr_file in "${filtered_bam_output_dir}"/*.bam; do
                if [[ "${bam_chr_file}" =~ REF_chr([XY0-9]+)\.bam ]]; then
                    chromosome="${BASH_REMATCH[1]}"
                    fasta_output="${fasta_output_dir}/${sample_name}_hap${hap}_chr${chromosome}.fasta"

                    # Convert BAM to FASTA using samtools
                    samtools fasta "${bam_chr_file}" > "${fasta_output}"

                    # Add chromosome annotation to the header of each sequence line in the FASTA file
                    awk -v chr="${chromosome}" '/^>/ { print $0 "|chr" chr } !/^>/ { print }' "${fasta_output}" > "${fasta_output}.tmp"
                    mv "${fasta_output}.tmp" "${fasta_output}"

                    echo "Converted ${bam_chr_file} to ${fasta_output}"
                fi
            done

            # Merge all FASTA files for the current haplotype into one file
            cat "${fasta_output_dir}/${sample_name}_hap${hap}_chr"*.fasta > "${fasta_output_dir}/${sample_name}_hap${hap}.fasta"
        done
    fi
done

echo "Conversion complete."
