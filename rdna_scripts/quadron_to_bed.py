import pandas as pd
import os
import subprocess
import glob

def collapse_intervals(input_bed_file, output_bed_file, q_column_index):
    # Sort the BED file
    sorted_bed_file = input_bed_file + '.sorted'
    sort_command = f'sort -k1,1 -k2,2n {input_bed_file} > {sorted_bed_file}'
    subprocess.run(sort_command, shell=True)

    # Merge overlapping intervals using bedtools and collapse the Q values
    bedtools_command = f'bedtools merge -i {sorted_bed_file} -c {q_column_index} -o collapse > {output_bed_file}'
    subprocess.run(bedtools_command, shell=True)

    # Remove the sorted temporary file
    os.remove(sorted_bed_file)

def process_csv_files(input_dir, output_dir):
    csv_files = glob.glob(os.path.join(input_dir, '*.csv'))

    for input_file in csv_files:
        # Read the CSV file
        df = pd.read_csv(input_file)

        # Calculate the stop value
        df['Start'] = df['Pos']
        df['Stop'] = df['Pos'] + df['L']

        # Select relevant columns for BED file
        bed_df = df[['Chromosome', 'Start', 'Stop', 'STR', 'Q']]

        # Split into two DataFrames based on STR value
        bed_df_plus = bed_df[bed_df['STR'] == '+'][['Chromosome', 'Start', 'Stop', 'Q']]
        bed_df_minus = bed_df[bed_df['STR'] == '-'][['Chromosome', 'Start', 'Stop', 'Q']]

        # Create output file paths
        base_name = os.path.basename(input_file).replace('.csv', '')
        output_file_plus = os.path.join(output_dir, f'{base_name}_pos.bed')
        output_file_minus = os.path.join(output_dir, f'{base_name}_neg.bed')

        # Output the BED files
        bed_df_plus.to_csv(output_file_plus, sep='\t', header=False, index=False)
        bed_df_minus.to_csv(output_file_minus, sep='\t', header=False, index=False)

        # Collapse overlapping intervals
        collapsed_output_file_plus = os.path.join(output_dir, f'{base_name}_pos_collapsed.bed')
        collapsed_output_file_minus = os.path.join(output_dir, f'{base_name}_neg_collapsed.bed')

        # The Q column is the 4th column in the BED files we generated (1-based index)
        q_column_index = 4

        collapse_intervals(output_file_plus, collapsed_output_file_plus, q_column_index)
        collapse_intervals(output_file_minus, collapsed_output_file_minus, q_column_index)

        print(f'Successfully created and collapsed BED files for {input_file}:\n{collapsed_output_file_plus}\n{collapsed_output_file_minus}')

# Specify the input directory and output directory
input_dir = '/home/alextu/scratch/rdna_analysis/rDNA_extracted_chm13_ref_genome/quadron_q19_filtered_csv'
output_dir = '/home/alextu/scratch/rdna_analysis/rDNA_extracted_chm13_ref_genome/collapsed_quadron_annotations_chm13'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process the CSV files
process_csv_files(input_dir, output_dir)
