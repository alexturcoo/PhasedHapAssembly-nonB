import os
import pandas as pd

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

# Define the chromosome sizes
chromosome_sizes = {
    'chr13': 3577493,
    'chr14': 718274,
    'chr15': 2201043,
    'chr21': 2504417,
    'chr22': 926856
}

# Main script
bed_files_directory = '/home/alextu/scratch/rdna_analysis/collapsed_quadron_annotations_verkko123_rdna/chr22'
output_combined_file = '/home/alextu/scratch/rdna_analysis/rdna_annotation_summary_stats/verkko_batch123_chm13_quadron_collapsed_summary_metrics_rdna_chr22.csv'

# Prepare list to hold the results
combined_results = []

# Iterate over all directories in the BED directory
for dirpath, dirnames, filenames in os.walk(bed_files_directory):
    chrom = os.path.basename(dirpath)
    if chrom not in chromosome_sizes:
        print(f"Chromosome {chrom} not found in the predefined sizes. Skipping directory.")
        continue
    
    genome_size = chromosome_sizes[chrom]
    print(f"Processing directory: {dirpath} with genome size: {genome_size}")

    # Iterate over all files in the current chromosome directory
    for filename in filenames:
        if filename.endswith('collapsed.bed'):
            print(f"Processing file: {filename}")
            parts = filename.split('_')
            sample = parts[0]  # Extract sample part from filename
            haplotype = parts[1]
            sample_haplotype = f"{sample}_{haplotype}"
            
            bed_file_path = os.path.join(dirpath, filename)
            total_count, total_bases_covered = process_bed_file(bed_file_path)
            if total_count is None:
                print(f"Skipping file due to processing error: {bed_file_path}")
                continue

            percent_of_genome = (total_bases_covered / genome_size) * 100
            motif_type = 'Positive_G_Quad' if 'pos' in filename else 'Negative_G_Quad' if 'neg' in filename else 'Unknown'
            combined_results.append((sample_haplotype, motif_type, total_count, total_bases_covered, percent_of_genome))
            print(f"Appended data: {(sample_haplotype, motif_type, total_count, total_bases_covered, percent_of_genome)}")

# Create DataFrame from the results
columns = ['Sample_Haplotype', 'Motif Type', 'Total Count', 'Total Bases Covered', 'Percent of Genome']
combined_metrics_df = pd.DataFrame(combined_results, columns=columns)

# Save the metrics DataFrame to a single CSV file
combined_metrics_df.to_csv(output_combined_file, index=False)

# Optionally, print a message indicating completion
print(f"Combined metrics CSV file has been created at {output_combined_file}.")
