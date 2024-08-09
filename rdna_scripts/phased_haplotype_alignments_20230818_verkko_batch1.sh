#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of nodes
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G # MEMORY PER NODE
#SBATCH --time=24:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=run_phased_hap_alignment_fasta
#SBATCH --output=run_phased_hap_alignment_fasta.o
#SBATCH --error=run_phased_hap_alignment_fasta.e

### THIS SCRIPT TAKES PHASED HAPLOTYPE ASSEMBLY ALIGNMENTS FROM
### 20230818_verkko_batch1 HGSVC SAMPLES AND CONVERTS THE ALIGNMENTS
### INTO FASTQ FILES WITH CHROMOSOME ANNOTATION FOR DOWNSTREAM ANALYSIS
module load samtools
module load bamtools

echo "Modules loaded: samtools, bamtools"

# Set the base directory containing subdirectories for each sample type
base_dir="/home/alextu/scratch/verkko_batch123_alignments_chm13"
echo "Base directory set to $base_dir"

# Specify the output base directory for filtered BAM files
bam_output_base="/home/alextu/scratch/rdna_analysis/rdna_filtered_chr_bams"
echo "Output base directory for BAM files set to $bam_output_base"

# Specify the output base directory for FASTA files
fasta_output_base="/home/alextu/scratch/rdna_analysis/rdna_filtered_chr_fasta"
echo "Output base directory for FASTA files set to $fasta_output_base"

# Chromosome and ranges to extract
declare -A ranges=(
    [chr13]="5770548-9348041"
    [chr14]="2099537-2817811"
    [chr15]="2506442-4707485"
    [chr21]="3108298-5612715"
    [chr22]="4793794-5720650"
)
echo "Chromosome ranges initialized for extraction"

# Loop over subdirectories (each corresponding to a sample type)
for sample_dir in "${base_dir}"/*/; do
    if [[ -d "${sample_dir}" ]]; then
        # Extract the sample name (e.g., HG00268) from the subdirectory path
        sample_name=$(basename "${sample_dir}")
        echo "Processing sample: $sample_name"

        # Create output directory for filtered BAM files based on sample name
        filtered_bam_output_dir="${bam_output_base}/${sample_name}"
        mkdir -p "${filtered_bam_output_dir}"
        echo "Created output directory for filtered BAM files: $filtered_bam_output_dir"

        # Create output directory for FASTA files based on sample name
        fasta_output_dir="${fasta_output_base}/${sample_name}"
        mkdir -p "${fasta_output_dir}"
        echo "Created output directory for FASTA files: $fasta_output_dir"

        # Construct the input BAM file path for the current sample type
        input_bam="${sample_dir}${sample_name}.vrk-ps-sseq.asm-rdna.t2tv2.sort.bam"
        echo "Input BAM file set to $input_bam"

        for chr in "${!ranges[@]}"; do
            range="${ranges[$chr]}"
            output_bam="${filtered_bam_output_dir}/${sample_name}_rdna_${chr}.bam"
            fasta_output="${fasta_output_dir}/${sample_name}_rdna_${chr}.fasta"

            # Extract specific chromosome range and convert to BAM, filtering for primary alignments (FLAG 256 off) with quality 0+
            echo "Extracting ${chr}:${range} from $input_bam"
            samtools view -b -F 256 -q 0 "${input_bam}" "${chr}:${range}" > "${output_bam}"
            echo "Extracted range ${range} for ${chr} with primary alignments only, saved to ${output_bam}"

            # Convert extracted BAM to FASTA
            echo "Converting $output_bam to FASTA format"
            samtools fasta "${output_bam}" > "${fasta_output}"
            echo "Converted ${output_bam} to ${fasta_output}"
        done
    fi
done

echo "Conversion complete. All tasks done."
