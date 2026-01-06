import pandas as pd
import glob
import os

# Define input and output directories
input_dir = '/home/alextu/scratch/extract_sv_flanks_2000bp/extracted_flanks/'
output_dir = '/home/alextu/scratch/extract_sv_flanks_2000bp/fasta_flanks/'

# Get all CSV files in the input directory
csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

# Iterate over each CSV file
for file_path in csv_files:
    # Extract the sample name from the filename (e.g., 'HG00096_hap1_SVflanks')
    file_name = os.path.basename(file_path).replace('.csv', '')

    # Remove '_SVflanks' from the file name
    file_name = file_name.replace('_SVflanks', '')

    # Load the CSV file
    df = pd.read_csv(file_path)

    # Define the output FASTA file path
    output_fasta = os.path.join(output_dir, f'flanking_sequences_{file_name}.fasta')

    # Open a new FASTA file for writing
    with open(output_fasta, 'w') as fasta_file:
        # Iterate through the DataFrame two rows at a time
        for i in range(0, len(df), 2):
            # Ensure there are two rows to process
            if i + 1 < len(df):
                # Get pre-flank and post-flank rows
                pre_flank_row = df.iloc[i]
                post_flank_row = df.iloc[i + 1]

                # Extract information for pre-flank
                region_pre = pre_flank_row['Region']
                sv_type_pre = pre_flank_row['SV Type']
                flank_seq_pre = pre_flank_row['Flanking Sequence']

                # Write pre-flank to FASTA with | separator
                fasta_file.write(f'>{region_pre}|{sv_type_pre}|pre_flank\n')
                fasta_file.write(f'{flank_seq_pre}\n')

                # Extract information for post-flank
                region_post = post_flank_row['Region']
                sv_type_post = post_flank_row['SV Type']
                flank_seq_post = post_flank_row['Flanking Sequence']

                # Write post-flank to FASTA with | separator
                fasta_file.write(f'>{region_post}|{sv_type_post}|post_flank\n')
                fasta_file.write(f'{flank_seq_post}\n')

    print(f'FASTA file created: {output_fasta}')