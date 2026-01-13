import os
import pandas as pd

# Commented out the get_genome_size function as it is no longer needed
# def get_genome_size(fasta_file, exclude_ns=False):
#     """Calculate the total size of the genome from a fasta file."""
#     total_size = 0
#     with open(fasta_file, 'r') as file:
#         for line in file:
#             if line.startswith('>'):
#                 continue
#             if exclude_ns:
#                 total_size += len(line.strip().replace('N', ''))
#             else:
#                 total_size += len(line.strip())
#     return total_size

def process_bed_file(file_path):
    """Process a BED file to calculate total count and total bases covered."""
    print(f"Processing BED file: {file_path}")  # Debug statement
    df = pd.read_csv(file_path, sep='\t', header=None, names=['chrom', 'start', 'end'], comment='#')
    print(f"Loaded {len(df)} rows from {file_path}")  # Debug statement
    return df

# Main script
bed_files_directory = '/home/alextu/scratch/mei_analysis/annotated_flanks_nbmst_collapsed'
output_file = '/home/alextu/scratch/mei_analysis/MEIflanks_collapsed_summary_metrics_chr.csv'

# Commented out the fasta_directory and fasta_extension as they are no longer needed
# fasta_directory = '/home/alextu/scratch/filtered_chr_fasta/chm13/chm13_verkko_batch123_all_fastas'
# fasta_extension = '.fasta'  # Change this if the extension is different

# Prepare a list to hold the results
results = []

# Iterate over all subdirectories
print(f"Iterating over directory: {bed_files_directory}")  # Debug statement
for haplotype_dir in os.listdir(bed_files_directory):
    haplotype_dir_path = os.path.join(bed_files_directory, haplotype_dir)
    if os.path.isdir(haplotype_dir_path):
        print(f"Processing haplotype directory: {haplotype_dir_path}")  # Debug statement
        # Commented out the lines related to fasta file processing
        # Determine the corresponding fasta file
        # fasta_file_path = os.path.join(fasta_directory, haplotype_dir + fasta_extension)
        # if os.path.exists(fasta_file_path):
        #     genome_size = get_genome_size(fasta_file_path, exclude_ns=False)  # Set exclude_ns as needed
        for filename in os.listdir(haplotype_dir_path):
            if filename.endswith('.bed'):
                motif_type = filename.split('.')[0]  # Extract motif type from filename
                bed_file_path = os.path.join(haplotype_dir_path, filename)
                print(f"Found BED file: {bed_file_path}, Motif Type: {motif_type}")  # Debug statement
                df = process_bed_file(bed_file_path)
                grouped = df.groupby('chrom')
                for chrom, group in grouped:
                    total_count = len(group)
                    total_bases_covered = (group['end'] - group['start']).sum()
                    # Commented out the calculation of percent_of_genome
                    # percent_of_genome = (total_bases_covered / genome_size) * 100
                    sample_haplotype_chrom = f"{haplotype_dir}|{chrom}"
                    # Adjusted to remove percent_of_genome from the results
                    results.append((sample_haplotype_chrom, motif_type, total_count, total_bases_covered))
                    print(f"Chromosome: {chrom}, Total Count: {total_count}, Total Bases Covered: {total_bases_covered}")  # Debug statement

# Create a DataFrame from the results
# Adjusted to remove the Percent of Genome column
columns = ['Sample_Haplotype_Chromosome', 'Motif Type', 'Total Count', 'Total Bases Covered']
metrics_df = pd.DataFrame(results, columns=columns)

# Save the metrics DataFrame to a CSV file
print(f"Saving metrics to {output_file}")  # Debug statement
metrics_df.to_csv(output_file, index=False)

# Optionally, print a message indicating completion
print(f"Metrics CSV file has been created at {output_file}.")