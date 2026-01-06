import pandas as pd
import os

# Define input and output paths
input_file = '/home/alextu/scratch/mei_analysis/MEI_Callset_T2T-CHM13.ALL.20240918.csv'  # Replace with your actual file path
output_dir = '/home/alextu/scratch/mei_analysis/hapspecific_fasta_files_MEIs'  # Define output directory
os.makedirs(output_dir, exist_ok=True)

# Load the MEI callset
mei_df = pd.read_csv(input_file)

# Extract columns starting with 'HG' or 'NA'
sample_columns = [col for col in mei_df.columns if col.startswith(('HG', 'NA'))]

# Iterate through each sample column to create output FASTA files
for sample in sample_columns:
    hap1_file = os.path.join(output_dir, f'{sample}.h1.MEI.fasta')
    hap2_file = os.path.join(output_dir, f'{sample}.h2.MEI.fasta')
    
    with open(hap1_file, 'w') as h1, open(hap2_file, 'w') as h2:
        for index, row in mei_df.iterrows():
            # Get the genotype call for the current sample
            genotype = row[sample]
            
            # Parse required information
            chrom = row['CHROM']
            pos = int(row['POS'])
            te_designation = row['TE_Designation']
            l1me_aid_info = row['L1ME-AID_INFO']
            alt = row['ALT']  # Insertion sequence
            
            # Calculate insertion size
            ins_size = len(alt)
            mei_id = f'{chrom}_{pos}_{ins_size}_INS'
            
            # FASTA header line
            fasta_header = f'>{mei_id} | CHROM: {chrom} | POS: {pos} | TE: {te_designation} | INFO: {l1me_aid_info}'
            
            # Depending on genotype, write to the appropriate FASTA file
            if genotype == '1|0|.':  # MEI in hap1
                h1.write(f'{fasta_header}\n{alt}\n')
            elif genotype == '0|1|.':  # MEI in hap2
                h2.write(f'{fasta_header}\n{alt}\n')
            elif genotype == '1|1|.':  # MEI in both hap1 and hap2
                h1.write(f'{fasta_header}\n{alt}\n')
                h2.write(f'{fasta_header}\n{alt}\n')

print("FASTA files created successfully!")
