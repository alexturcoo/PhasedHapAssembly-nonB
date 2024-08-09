#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 #specify number of gpus
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G # MEMORY PER NODE
#SBATCH --time=1:00:00 #hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com #sends me an email once done
#SBATCH --job-name=extract_rdna_chm13
#SBATCH --output=extract_rdna_chm13.o
#SBATCH --error=extract_rdna_chm13.e

module load samtools

# Define the path to your CHM13 fasta file
CHM13_FASTA="/home/alextu/scratch/reference_genomes/ref_genome_chm13_hprc/chm13v2.0.fa"

# Create an output directory for intermediate files
mkdir -p rDNA_extracted

# Extract the regions
samtools faidx $CHM13_FASTA chr13:5770548-9348041 > rDNA_extracted/chr13_5770548_9348041.fasta
samtools faidx $CHM13_FASTA chr14:2099537-2817811 > rDNA_extracted/chr14_2099537_2817811.fasta
samtools faidx $CHM13_FASTA chr15:2506442-4707485 > rDNA_extracted/chr15_2506442_4707485.fasta
samtools faidx $CHM13_FASTA chr21:3108298-5612715 > rDNA_extracted/chr21_3108298_5612715.fasta
samtools faidx $CHM13_FASTA chr22:4793794-5720650 > rDNA_extracted/chr22_4793794_5720650.fasta

# Concatenate the extracted regions into a single fasta file with appropriate headers
cat rDNA_extracted/chr13_5770548_9348041.fasta | sed 's/>.*/>chr13_5770548_9348041/' > rDNA_extracted/all_rDNA_regions.fasta
cat rDNA_extracted/chr14_2099537_2817811.fasta | sed 's/>.*/>chr14_2099537_2817811/' >> rDNA_extracted/all_rDNA_regions.fasta
cat rDNA_extracted/chr15_2506442_4707485.fasta | sed 's/>.*/>chr15_2506442_4707485/' >> rDNA_extracted/all_rDNA_regions.fasta
cat rDNA_extracted/chr21_3108298_5612715.fasta | sed 's/>.*/>chr21_3108298_5612715/' >> rDNA_extracted/all_rDNA_regions.fasta
cat rDNA_extracted/chr22_4793794_5720650.fasta | sed 's/>.*/>chr22_4793794_5720650/' >> rDNA_extracted/all_rDNA_regions.fasta

# The final fasta file with all the rDNA regions
echo "All rDNA regions have been extracted to: rDNA_extracted/all_rDNA_regions.fasta"
