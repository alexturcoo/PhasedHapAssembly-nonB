import os
import pandas as pd

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
    df = pd.read_csv(file_path, sep='\t', header=None, names=['chrom', 'start', 'end'], comment='#')
    total_count = len(df)
    total_bases_covered = (df['end'] - df['start']).sum()
    return total_count, total_bases_covered

# Main script
bed_files_directory = '/home/alextu/scratch/nonb_motif_annotations_hgsvc/20240201_verkko_batch3_nonb_annotations_collapsed_chm13'
output_file = '/home/alextu/scratch/results/20240201_verkko_batch3_assemblies_aligned_chm13_collapsed/verkko_batch3_chm13_collapsed_summary_metrics.csv'

# Assuming fasta files are in the same directory and named correspondingly to haplotypes
fasta_directory = '/home/alextu/scratch/filtered_chr_fasta/20240201_verkko_batch3_align_chm13/all_fastas'
fasta_extension = '.fasta'  # Change this if the extension is different

# Prepare a list to hold the results
results = []

# Iterate over all subdirectories
for haplotype_dir in os.listdir(bed_files_directory):
    haplotype_dir_path = os.path.join(bed_files_directory, haplotype_dir)
    if os.path.isdir(haplotype_dir_path):
        # Determine the corresponding fasta file
        fasta_file_path = os.path.join(fasta_directory, haplotype_dir + fasta_extension)
        if os.path.exists(fasta_file_path):
            genome_size = get_genome_size(fasta_file_path, exclude_ns=False)  # Set exclude_ns as needed
            for filename in os.listdir(haplotype_dir_path):
                if filename.endswith('.bed'):
                    motif_type = filename.split('.')[0]  # Extract motif type from filename
                    bed_file_path = os.path.join(haplotype_dir_path, filename)
                    total_count, total_bases_covered = process_bed_file(bed_file_path)
                    percent_of_genome = (total_bases_covered / genome_size) * 100
                    results.append((haplotype_dir, motif_type, total_count, total_bases_covered, percent_of_genome))

# Create a DataFrame from the results
columns = ['Sample_Haplotype', 'Motif Type', 'Total Count', 'Total Bases Covered', 'Percent of Genome']
metrics_df = pd.DataFrame(results, columns=columns)

# Save the metrics DataFrame to a CSV file
metrics_df.to_csv(output_file, index=False)

# Optionally, print a message indicating completion
print(f"Metrics CSV file has been created at {output_file}.")
