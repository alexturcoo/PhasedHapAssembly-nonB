import pandas as pd
import os

# Define input and output paths
input_file = '/home/alextu/scratch/mei_analysis/MEI_Callset_T2T-CHM13.ALL.20240918.csv'  # Replace with your actual file path
output_dir = '/home/alextu/scratch/mei_analysis/mei_hap_specific_beds_flanks_withdesignations'  # Define output directory
os.makedirs(output_dir, exist_ok=True)

# Load the MEI callset
mei_df = pd.read_csv(input_file)

# Extract columns starting with 'HG' or 'NA'
sample_columns = [col for col in mei_df.columns if col.startswith(('HG', 'NA'))]

# Iterate through each sample column to create output BED files
for sample in sample_columns:
    # Create two output files for hap1 and hap2
    hap1_file = os.path.join(output_dir, f'{sample}.h1.MEIcoords2000flank_bedtools.bed')
    hap2_file = os.path.join(output_dir, f'{sample}.h2.MEIcoords2000flank_bedtools.bed')

    with open(hap1_file, 'w') as h1, open(hap2_file, 'w') as h2:
        # Iterate through each row of the MEI DataFrame
        for index, row in mei_df.iterrows():
            # Get the genotype call for the current sample
            genotype = row[sample]
            
            # Parse the ID, chromosome, position, ref, alt, TE designation, and L1ME-AID info from the current row
            chrom = row['CHROM']
            pos = int(row['POS'])
            ref = row['REF']
            alt = row['ALT']
            te_designation = row['TE_Designation']
            l1me_aid_info = row['L1ME-AID_INFO']
            
            # Restructure the ID
            ins_size = len(alt) - len(ref)  # Calculate insertion size
            mei_id = f'{chrom}_{pos}_{ins_size}_INS'

            # Define start and end positions for the 2000bp flanking regions
            upstream_start = pos - 2000
            upstream_end = pos
            downstream_start = pos
            downstream_end = pos + 2000

            # Depending on the genotype, write to the appropriate BED file
            if genotype == '1|0|.':  # MEI in hap1
                h1.write(f'{chrom}\t{upstream_start}\t{upstream_end}\t{mei_id}\t{ref}\t{alt}\t{te_designation}\t{l1me_aid_info}\n')
                h1.write(f'{chrom}\t{downstream_start}\t{downstream_end}\t{mei_id}\t{ref}\t{alt}\t{te_designation}\t{l1me_aid_info}\n')
            elif genotype == '0|1|.':  # MEI in hap2
                h2.write(f'{chrom}\t{upstream_start}\t{upstream_end}\t{mei_id}\t{ref}\t{alt}\t{te_designation}\t{l1me_aid_info}\n')
                h2.write(f'{chrom}\t{downstream_start}\t{downstream_end}\t{mei_id}\t{ref}\t{alt}\t{te_designation}\t{l1me_aid_info}\n')
            elif genotype == '1|1|.':  # MEI in both hap1 and hap2
                h1.write(f'{chrom}\t{upstream_start}\t{upstream_end}\t{mei_id}\t{ref}\t{alt}\t{te_designation}\t{l1me_aid_info}\n')
                h1.write(f'{chrom}\t{downstream_start}\t{downstream_end}\t{mei_id}\t{ref}\t{alt}\t{te_designation}\t{l1me_aid_info}\n')
                h2.write(f'{chrom}\t{upstream_start}\t{upstream_end}\t{mei_id}\t{ref}\t{alt}\t{te_designation}\t{l1me_aid_info}\n')
                h2.write(f'{chrom}\t{downstream_start}\t{downstream_end}\t{mei_id}\t{ref}\t{alt}\t{te_designation}\t{l1me_aid_info}\n')

print("BED files created successfully!")