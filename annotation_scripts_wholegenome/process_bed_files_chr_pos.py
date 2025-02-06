import os
import pandas as pd

def process_bed_file(file_path, directory_name, motif_type):
    """Process a BED file and prepend the directory name to the first column."""
    print(f"Processing BED file: {file_path}")  # Debug statement
    # Read the BED file
    df = pd.read_csv(file_path, sep='\t', header=None, names=['name', 'start', 'end'], comment='#')
    print(f"Loaded {len(df)} rows from {file_path}")  # Debug statement
    # Prepend the directory name to the `name` column
    df['name'] = f"{directory_name}|" + df['name']
    # Add the Motif Type column
    df['motif_type'] = motif_type
    return df

# Main script
main_directory = '/home/alextu/scratch/extract_sv_flanks_2000bp/annotated_flanks_nbmst_collapsed'  # Replace with your main directory
output_file = '/home/alextu/scratch/extract_sv_flanks_2000bp/SVflanks_collapsed_summary_metrics_chr_position.csv'

# Prepare a list to hold the results
results = []

# Iterate over all subdirectories
print(f"Iterating over directory: {main_directory}")  # Debug statement
for subdirectory in os.listdir(main_directory):
    subdirectory_path = os.path.join(main_directory, subdirectory)
    if os.path.isdir(subdirectory_path):
        print(f"Processing subdirectory: {subdirectory_path}")  # Debug statement
        for filename in os.listdir(subdirectory_path):
            if filename.endswith('.bed'):
                motif_type = filename.split('.')[0]  # Extract motif type from filename
                bed_file_path = os.path.join(subdirectory_path, filename)
                print(f"Found BED file: {bed_file_path}, Motif Type: {motif_type}")  # Debug statement
                df = process_bed_file(bed_file_path, subdirectory, motif_type)
                for _, row in df.iterrows():
                    # Append each record to results
                    results.append({
                        'Sample_Haplotype_Chromosome': row['name'],
                        'Motif Type': row['motif_type'],
                        'Start': row['start'],
                        'End': row['end']
                    })

# Create a DataFrame from the results
columns = ['Sample_Haplotype_Chromosome', 'Motif Type', 'Start', 'End']
output_df = pd.DataFrame(results, columns=columns)

# Save the DataFrame to a CSV file
print(f"Saving output to {output_file}")  # Debug statement
output_df.to_csv(output_file, index=False, sep=',', header=True)

# Optionally, print a message indicating completion
print(f"Summary CSV file has been created at {output_file}.")