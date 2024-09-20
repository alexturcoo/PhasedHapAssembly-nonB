import pandas as pd
import subprocess
import os
import glob

def process_haplotype_files(haplotype_dir, feature, output_base_dir, sample_name):
    """
    Process specific feature files from each haplotype directory and merge overlapping intervals.

    Parameters:
    haplotype_dir (str): The path to the haplotype directory.
    feature (str): The feature type (e.g., 'APR', 'DR', 'IR', 'MR', 'Z').
    output_base_dir (str): The base directory to output processed files.
    sample_name (str): The sample name prefix for the TSV files.

    Returns:
    None
    """
    
    # Construct the file path for the specific feature
    file_path = os.path.join(haplotype_dir, f'{sample_name}_{feature}.tsv')
    
    print(f'Processing file: {file_path}')
    if os.path.exists(file_path):
        try:
            # Load the file with tab-delimited columns
            feature_data = pd.read_csv(file_path, delimiter="\t")
            
            # If the file is empty, skip processing
            if feature_data.empty:
                print(f'File is empty: {file_path}')
                return
            
            # Extract necessary columns:
            feature_data = feature_data[['Sequence_name', 'Start', 'Stop']]
            
            # Count the number of motifs before collapsing
            pre_collapse_count = feature_data.shape[0]
            
            # Construct the output directory and file path
            haplotype_output_dir = f'{output_base_dir}/{sample_name}'
            os.makedirs(haplotype_output_dir, exist_ok=True)
            output_file_path = f'{haplotype_output_dir}/{feature}.collapsed.bed'
            
            print(f'Output directory: {haplotype_output_dir}')
            print(f'Output file path: {output_file_path}')
            
            # Save the processed data to a temporary file without the header and index
            temp_file_path = f'{haplotype_output_dir}/{feature}.temp.bed'
            feature_data.to_csv(temp_file_path, sep='\t', index=False, header=False)
            
            # Sort the temporary file
            sorted_temp_file_path = f'{haplotype_output_dir}/{feature}.sorted.temp.bed'
            sort_command = f'sort -k1,1 -k2,2n {temp_file_path} > {sorted_temp_file_path}'
            print(f'Running sort command: {sort_command}')
            subprocess.run(sort_command, shell=True)
            
            # Merge overlapping intervals using bedtools
            bedtools_command = f'bedtools merge -i {sorted_temp_file_path} > {output_file_path}'
            print(f'Running bedtools command: {bedtools_command}')
            subprocess.run(bedtools_command, shell=True)
            
            # Remove the temporary files
            os.remove(temp_file_path)
            os.remove(sorted_temp_file_path)
            
            # Count the number of motifs after collapsing
            if os.path.exists(output_file_path) and os.path.getsize(output_file_path) > 0:
                merged_data = pd.read_csv(output_file_path, delimiter="\t", header=None)
                post_collapse_count = merged_data.shape[0]
            else:
                post_collapse_count = 0
            
            # Print the count of motifs before and after collapsing
            print(f'Feature: {feature} | Sample: {sample_name} | Pre-collapse count: {pre_collapse_count} | Post-collapse count: {post_collapse_count}')
        
        except pd.errors.EmptyDataError:
            print(f'File is empty: {file_path}')
    else:
        print(f'File not found: {file_path}')

def process_all_haplotypes(base_dir, features, output_base_dir):
    """
    Process specified feature files from all haplotype directories.

    Parameters:
    base_dir (str): The base directory containing haplotype directories.
    features (list): List of feature types to process.
    output_base_dir (str): The base directory to output processed files.

    Returns:
    None
    """
    
    # Get all haplotype directories starting with "HG" or "NA"
    haplotype_dirs = glob.glob(os.path.join(base_dir, '*chr*'))
    
    print(f'Found haplotype directories: {haplotype_dirs}')
    for haplotype_dir in haplotype_dirs:
        sample_name = os.path.basename(haplotype_dir)
        print(f'Processing sample: {sample_name}')
        for feature in features:
            process_haplotype_files(haplotype_dir, feature, output_base_dir, sample_name)

# Define the base directory containing haplotype directories
base_dir = '/home/alextu/scratch/centromere_analysis/verkko123_nBMST_active_asat_HOR_arrays_annotations/'

# Define the base directory to output processed files
output_base_dir = '/home/alextu/scratch/centromere_analysis/verkko123_nBMST_active_asat_HOR_arrays_annotations_collapsed/'

# Define the list of features to process
features = ['DR', 'IR', 'MR', 'Z', 'APR']

# Define the list of chromosomes to iterate over (e.g., chr1 to chr22 and chrX, chrY)
chromosomes = [f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY']
#chromosomes = ["chr7"]

# Iterate over all chromosomes
for chromosome in chromosomes:
    # Update the paths for the current chromosome
    current_base_dir = f'{base_dir}{chromosome}'
    current_output_base_dir = f'{output_base_dir}{chromosome}'

    # Process all haplotype directories for the current chromosome
    process_all_haplotypes(current_base_dir, features, current_output_base_dir)

