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
    df = pd.read_csv(file_path, sep='\t', header=None, names=['chrom', 'start', 'end'], comment='#')
    return df

# List of chromosome identifiers you want to process
chromosomes = [f"chr{i}" for i in range(1, 23)] + ['chrX', 'chrY']

# Main script
# Commented out the fasta_directory and fasta_extension as they are no longer needed
# fasta_directory = '/home/alextu/scratch/filtered_chr_fasta/chm13/chm13_verkko_batch123_all_fastas'
# fasta_extension = '.fasta'  # Change this if the extension is different

# Iterate over each chromosome
for chromosome in chromosomes:
    bed_files_directory = f'/home/alextu/scratch/centromere_analysis/verkko123_nBMST_active_asat_HOR_arrays_annotations_collapsed/{chromosome}'
    output_file = f'/home/alextu/scratch/centromere_analysis/summary_stats/haplotype_summarystats_verkko123_active_asat_HOR_arrays/verkko123_collapsed_summary_metrics_centromere_{chromosome}.csv'
    
    # Prepare a list to hold the results
    results = []

    # Iterate over all subdirectories
    for haplotype_dir in os.listdir(bed_files_directory):
        haplotype_dir_path = os.path.join(bed_files_directory, haplotype_dir)
        if os.path.isdir(haplotype_dir_path):
            # Commented out the lines related to fasta file processing
            # Determine the corresponding fasta file
            # fasta_file_path = os.path.join(fasta_directory, haplotype_dir + fasta_extension)
            # if os.path.exists(fasta_file_path):
            #     genome_size = get_genome_size(fasta_file_path, exclude_ns=False)  # Set exclude_ns as needed
            for filename in os.listdir(haplotype_dir_path):
                if filename.endswith('.bed'):
                    motif_type = filename.split('.')[0]  # Extract motif type from filename
                    bed_file_path = os.path.join(haplotype_dir_path, filename)
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

    # Create a DataFrame from the results
    # Adjusted to remove the Percent of Genome column
    columns = ['Sample_Haplotype_Chromosome', 'Motif Type', 'Total Count', 'Total Bases Covered']
    metrics_df = pd.DataFrame(results, columns=columns)

    # Save the metrics DataFrame to a CSV file
    metrics_df.to_csv(output_file, index=False)

    # Clear the results list after saving
    results.clear()

    # Optionally, print a message indicating completion
    print(f"Metrics CSV file has been created for {chromosome} at {output_file}.")
