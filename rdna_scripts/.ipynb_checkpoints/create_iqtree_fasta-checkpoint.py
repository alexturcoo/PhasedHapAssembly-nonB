import os
import re

# Define the directory containing the fasta files
base_dir = '/home/alextu/scratch/rdna_analysis/rdna_filtered_chr_fasta_2_N/chr14'

# Define the output file
output_file = '/home/alextu/scratch/rdna_analysis/rdna_filtered_chr_fasta_2_N/chr14/combined_rdna_sequences_chr14_verkko123.fasta'

# Function to process each fasta file
def process_fasta(file_path, sample_id):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Append the sample ID to the existing header
        lines[0] = lines[0].strip() + f'_{sample_id}\n'
    return lines

# Initialize an empty list to store the processed fasta entries
combined_fasta = []

# Walk through the files in the directory
for file in os.listdir(base_dir):
    if file.endswith('.fasta'):
        # Use regex to extract the sample ID (either HG#### or NA####) from the filename
        sample_id = re.search(r'(HG\d+|NA\d+)', file).group(0)
        file_path = os.path.join(base_dir, file)
        # Process the fasta file and add it to the list
        combined_fasta.extend(process_fasta(file_path, sample_id))

# Write the combined fasta entries to the output file
with open(output_file, 'w') as outfile:
    for entry in combined_fasta:
        outfile.writelines(entry)

print("Fasta files have been combined and written to", output_file)
