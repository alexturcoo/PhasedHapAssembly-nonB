import os
import pandas as pd

### This script generates genome-statistics per haplotype for Quadron based annotations.

def get_genome_size(fasta_file, exclude_ns=False):
    """Calculate the total size of the genome from a fasta file."""
    total_size = 0
    with open(fasta_file, 'r') as file:
        for line in file:
            if line.startswith('>'):
                continue
            if exclude_ns:
                total_size += len(line.strip().replace('N', ''))
            else:
                total_size += len(line.strip())
    return total_size

def process_bed_file(file_path):
    """Process a BED file to calculate total count and total bases covered."""
    # Read only the first three columns from the BED file and ignore others
    try:
        df = pd.read_csv(file_path, sep='\t', header=None, usecols=[0, 1, 2], names=['chrom', 'start', 'end'], dtype={'chrom': str, 'start': 'int64', 'end': 'int64'}, comment='#')
    except ValueError as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None

    # Drop rows with NaN values in 'start' and 'end' columns
    df.dropna(subset=['start', 'end'], inplace=True)
    
    total_count = len(df)
    total_bases_covered = (df['end'] - df['start']).sum()
    return total_count, total_bases_covered

# Main script
bed_files_directory = '/home/alextu/scratch/results/bed_files/all_quadron_beds_verkko_batch123_collapsed_chm13'
output_combined_file = '/home/alextu/scratch/results/summary_stats/verkko_batch123_chm13_collapsed_quadron_summary_metrics_combined.csv'

# Assuming fasta files are in the same directory and named correspondingly to haplotypes
fasta_directory = '/home/alextu/scratch/filtered_chr_fasta/chm13_verkko_batch123_all_fastas'
fasta_extension = '.fasta'  # Change this if the extension is different

# Prepare list to hold the results
combined_results = []

# Iterate over all files in the BED directory
for filename in os.listdir(bed_files_directory):
    if filename.endswith('.bed'):
        print(f"Processing file: {filename}")
        parts = filename.split('_')
        sample = parts[0]  # Extract sample part from filename
        haplotype = parts[1]
        sample_haplotype = f"{sample}_{haplotype}"
        fasta_file_name = f"{sample}_{haplotype}{fasta_extension}"
        fasta_file_path = os.path.join(fasta_directory, fasta_file_name)
        
        print(f"Fasta file being worked on: {fasta_file_path}")
        
        if os.path.exists(fasta_file_path):
            genome_size = get_genome_size(fasta_file_path, exclude_ns=False)  # Set exclude_ns as needed
            bed_file_path = os.path.join(bed_files_directory, filename)
            total_count, total_bases_covered = process_bed_file(bed_file_path)
            if total_count is None:
                print(f"Skipping file due to processing error: {bed_file_path}")
                continue
            percent_of_genome = (total_bases_covered / genome_size) * 100
            if 'pos' in filename:
                motif_type = 'Positive_G_Quad'
            elif 'neg' in filename:
                motif_type = 'Negative_G_Quad'
            else:
                motif_type = 'Unknown'  # Handle unexpected cases
            combined_results.append((sample_haplotype, motif_type, total_count, total_bases_covered, percent_of_genome))
            print(f"Appended data: {(sample_haplotype, motif_type, total_count, total_bases_covered, percent_of_genome)}")
        else:
            print(f"Fasta file not found for: {fasta_file_name}")

# Create DataFrame from the results
columns = ['Sample_Haplotype', 'Motif Type', 'Total Count', 'Total Bases Covered', 'Percent of Genome']
combined_metrics_df = pd.DataFrame(combined_results, columns=columns)

# Save the metrics DataFrame to a single CSV file
combined_metrics_df.to_csv(output_combined_file, index=False)

# Optionally, print a message indicating completion
print(f"Combined metrics CSV file has been created at {output_combined_file}.")
