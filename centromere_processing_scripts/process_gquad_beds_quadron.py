import os
import pandas as pd

def process_bed_file(file_path):
    """Process a BED file to calculate total count and total base coverage."""
    # Read only the first three columns from the BED file and ignore others
    try:
        df = pd.read_csv(file_path, sep='\t', header=None, usecols=[0, 1, 2], names=['chrom', 'start', 'end'], dtype={'chrom': str, 'start': 'int64', 'end': 'int64'}, comment='#')
    except ValueError as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None

    # Drop rows with NaN values in 'start' and 'end' columns
    df.dropna(subset=['start', 'end'], inplace=True)
    
    total_count = len(df)
    total_base_coverage = (df['end'] - df['start']).sum()
    return total_count, total_base_coverage

# Base directory containing all chromosome directories
base_bed_files_directory = '/home/alextu/scratch/centromere_analysis/verkko123_quadron_active_asat_HOR_arrays_collapsed'
base_output_combined_file = '/home/alextu/scratch/centromere_analysis/summary_stats/haplotype_summarystats_verkko123_active_asat_HOR_arrays'

# List of chromosome directories
chromosomes = [f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY']

# Iterate over each chromosome directory
for chromosome in chromosomes:
    bed_files_directory = os.path.join(base_bed_files_directory, chromosome)
    output_combined_file = os.path.join(base_output_combined_file, f'verkko123_quadron_collapsed_summary_metrics_centromeres_{chromosome}.csv')

    # Prepare list to hold the results
    combined_results = []

    # Iterate over all directories in the BED directory
    for dirpath, dirnames, filenames in os.walk(bed_files_directory):
        chrom = os.path.basename(dirpath)
        
        print(f"Processing directory: {dirpath}")

        # Iterate over all files in the current chromosome directory
        for filename in filenames:
            if filename.endswith('collapsed.bed'):
                print(f"Processing file: {filename}")
                parts = filename.split('_')
                sample = parts[0]  # Extract sample part from filename
                haplotype = parts[1]
                sample_haplotype = f"{sample}_{haplotype}"
                
                bed_file_path = os.path.join(dirpath, filename)
                total_count, total_base_coverage = process_bed_file(bed_file_path)
                if total_count is None:
                    print(f"Skipping file due to processing error: {bed_file_path}")
                    continue

                motif_type = 'Positive_G_Quad' if 'pos' in filename else 'Negative_G_Quad' if 'neg' in filename else 'Unknown'
                combined_results.append((sample_haplotype, motif_type, total_count, total_base_coverage))
                print(f"Appended data: {(sample_haplotype, motif_type, total_count, total_base_coverage)}")

    # Create DataFrame from the results
    columns = ['Sample_Haplotype', 'Motif Type', 'Total Count', 'Total Base Coverage']
    combined_metrics_df = pd.DataFrame(combined_results, columns=columns)

    # Save the metrics DataFrame to a single CSV file
    combined_metrics_df.to_csv(output_combined_file, index=False)

    # Optionally, print a message indicating completion
    print(f"Combined metrics CSV file has been created at {output_combined_file} for {chromosome}.")
