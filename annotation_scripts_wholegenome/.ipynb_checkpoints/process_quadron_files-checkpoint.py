import pandas as pd
import re
import os

### This script converts quadron outputted .txt file annotations into useable CSVs with all the corresponding data from Quadron

def extract_chromosome(file_name):
    match = re.search(r'chr[0-9XY]+', file_name)
    return match.group(0) if match else None

def extract_haplotype(file_name):
    match = re.search(r'hap[12]', file_name)
    return match.group(0) if match else None

def parse_file(file_path):
    chromosome = extract_chromosome(os.path.basename(file_path))
    haplotype = extract_haplotype(os.path.basename(file_path))
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
                
    return haplotype, data_rows

# Base directory containing all sample directories
base_directory_path = '/path/to/quadron/txt/files'

# Output base directory
output_base_directory = '/path/to/quadron/csvs'

# Iterate over each sample directory
for sample_dir in os.listdir(base_directory_path):
    sample_path = os.path.join(base_directory_path, sample_dir)
    
    if os.path.isdir(sample_path):
        all_data_hap1 = []
        all_data_hap2 = []

        for file_name in os.listdir(sample_path):
            file_path = os.path.join(sample_path, file_name)
            
            if os.path.isfile(file_path):
                haplotype, data_rows = parse_file(file_path)
                
                if haplotype == 'hap1':
                    all_data_hap1.extend(data_rows)
                elif haplotype == 'hap2':
                    all_data_hap2.extend(data_rows)

        if all_data_hap1:
            column_names = ['Chromosome', 'Pos', 'STR', 'L', 'Q', 'Sequence']
            df_hap1 = pd.DataFrame(all_data_hap1, columns=column_names)
            df_hap1['Q'] = pd.to_numeric(df_hap1['Q'], errors='coerce')
            filtered_df_hap1 = df_hap1[df_hap1['Q'] > 19]

            #output_dir_hap1 = os.path.join(output_base_directory, sample_dir, 'hap1')
            #os.makedirs(output_dir_hap1, exist_ok=True)

            output_file_hap1 = os.path.join(output_base_directory, f'{sample_dir}_hap1_quadron_filtered_verkko_batch3.csv')
            filtered_df_hap1.to_csv(output_file_hap1, index=False)

            print(f'Processed {sample_dir} hap1:')
            #print(filtered_df_hap1.head())

        if all_data_hap2:
            column_names = ['Chromosome', 'Pos', 'STR', 'L', 'Q', 'Sequence']
            df_hap2 = pd.DataFrame(all_data_hap2, columns=column_names)
            df_hap2['Q'] = pd.to_numeric(df_hap2['Q'], errors='coerce')
            filtered_df_hap2 = df_hap2[df_hap2['Q'] > 19]

            #output_dir_hap2 = os.path.join(output_base_directory, sample_dir, 'hap2')
            #os.makedirs(output_dir_hap2, exist_ok=True)

            output_file_hap2 = os.path.join(output_base_directory, f'{sample_dir}_hap2_quadron_filtered_verkko_batch3.csv')
            filtered_df_hap2.to_csv(output_file_hap2, index=False)

            print(f'Processed {sample_dir} hap2:')
            #print(filtered_df_hap2.head())
