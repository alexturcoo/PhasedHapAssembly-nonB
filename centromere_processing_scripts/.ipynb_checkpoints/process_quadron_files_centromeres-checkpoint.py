import pandas as pd
import re
import os

def extract_chromosome(file_name):
    match = re.search(r'chr[0-9XY]+', file_name)
    return match.group(0) if match else None

def parse_file(file_path):
    chromosome = extract_chromosome(os.path.basename(file_path))
    data_rows = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('DATA:'):
                parts = line.split()
                pos = parts[1]
                str_ = parts[2]
                l = parts[3]
                q = parts[4]
                sequence = parts[5]
                data_rows.append([chromosome, pos, str_, l, q, sequence])
                
    return data_rows

# Base directory containing all chromosome directories
base_directory_path = '/home/alextu/scratch/centromere_analysis/verkko123_quadron_active_asat_HOR_arrays'

# Output base directory
output_base_directory = '/home/alextu/scratch/centromere_analysis/verkko123_quadron_q19_active_asat_HOR_arrays_filtered_csv'

# List of chromosome directories
chromosomes = [f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY']

# Iterate over each chromosome directory
for chromosome in chromosomes:
    input_dir = os.path.join(base_directory_path, chromosome)
    output_dir = os.path.join(output_base_directory, chromosome)

    # Check if output directory exists, create if not
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over each file in the current chromosome directory
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        
        if os.path.isfile(file_path):
            print(f"Processing file: {file_path}")
            data_rows = parse_file(file_path)
            
            if data_rows:
                column_names = ['Chromosome', 'Pos', 'STR', 'L', 'Q', 'Sequence']
                df = pd.DataFrame(data_rows, columns=column_names)
                df['Q'] = pd.to_numeric(df['Q'], errors='coerce')
                filtered_df = df[df['Q'] > 19]

                # Ensure the output filename matches the input filename with a new extension
                output_file_name = os.path.splitext(file_name)[0] + '_filtered.csv'
                output_file = os.path.join(output_dir, output_file_name)
                print(f"Saving filtered data to: {output_file}")
                filtered_df.to_csv(output_file, index=False)

                print(f'Processed {len(filtered_df)} rows in {file_name} after filtering.')
            else:
                print(f"No data found in {file_name}")
