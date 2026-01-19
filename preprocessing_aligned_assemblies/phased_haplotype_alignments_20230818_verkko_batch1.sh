#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=24:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com
#SBATCH --job-name=run_phased_hap_alignment_fasta
#SBATCH --output=run_phased_hap_alignment_fasta.o
#SBATCH --error=run_phased_hap_alignment_fasta.e

### THIS SCRIPT TAKES PHASED HAPLOTYPE ASSEMBLY ALIGNMENTS FROM HGSVC3 VERKKO ALIGNED ASSEMBLIES BATCH 1,2,3
### CONVERTS THE ALIGNMENTS INTO FASTA FILES WITH CHROMOSOME ANNOTATION FOR DOWNSTREAM ANALYSIS
### Output will give you filtered BAM files as well as haplotype level FASTA FILES for non-B Annotation

module load samtools
module load bamtools

# Update for new batches
base_dir="/path/to/hgsvc3/samples/folder/"
bam_output_base="/path/to/bam/outputfolder/"
fasta_output_base="/path/to/fasta/outputfolder/"

for sample_dir in "${base_dir}"/*/; do
    if [[ -d "${sample_dir}" ]]; then
        sample_name=$(basename "${sample_dir}")

        filtered_bam_output_dir="${bam_output_base}/${sample_name}"
        mkdir -p "${filtered_bam_output_dir}"

        for hap in 1 2; do
            input_bam="${sample_dir}/${sample_name}.vrk-ps-sseq.asm-hap${hap}.hg38.sort.bam"
            output_primary_bam="${filtered_bam_output_dir}/${sample_name}_hap${hap}_primary.bam"

            # Filter BAM based on alignment quality
            samtools view -b -F 256 -q 0 "${input_bam}" > "${output_primary_bam}"

            # Split BAM by chromosome
            bamtools split -in "${output_primary_bam}" -reference

            mv *REF_chr*.bam "${filtered_bam_output_dir}/"

            fasta_output_dir="${fasta_output_base}/${sample_name}"
            mkdir -p "${fasta_output_dir}"

            # Loop over split BAM files (by chromosome) and convert to FASTA
            for bam_chr_file in "${filtered_bam_output_dir}"/*.bam; do
                if [[ "${bam_chr_file}" =~ REF_chr([XY0-9]+)\.bam ]]; then
                    chromosome="${BASH_REMATCH[1]}"
                    fasta_output="${fasta_output_dir}/${sample_name}_hap${hap}_chr${chromosome}.fasta"

                    samtools fasta "${bam_chr_file}" > "${fasta_output}"

                    # Add chromosome annotation to header of each sequence line in FASTA file
                    awk -v chr="${chromosome}" '/^>/ { print $0 "|chr" chr } !/^>/ { print }' "${fasta_output}" > "${fasta_output}.tmp"
                    mv "${fasta_output}.tmp" "${fasta_output}"
                    
                fi
            done

            # Merge all FASTA files for haplotype into one file
            cat "${fasta_output_dir}/${sample_name}_hap${hap}_chr"*.fasta > "${fasta_output_dir}/${sample_name}_hap${hap}.fasta"
        done
    fi
done