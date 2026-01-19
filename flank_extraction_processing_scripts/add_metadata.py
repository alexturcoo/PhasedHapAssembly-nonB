import pandas as pd
import glob
import os

main_df = pd.read_csv('/home/alextu/scratch/mei_analysis/MEIflanks_collapsed_summary_metrics_chr_position.csv')

# Extract the identifier part from 'Sample_Haplotype_Chromosome' for easier matching
main_df['Sample_Haplotype'] = main_df['Sample_Haplotype_Chromosome'].apply(lambda x: x.split('|')[0].replace('flanking_sequences_', ''))
main_df['Identifier'] = main_df['Sample_Haplotype_Chromosome'].apply(lambda x: x.split('|')[2])

# Replace 'h1' and 'h2' with 'hap1' and 'hap2' in Sample_Haplotype for consistency
main_df['Sample_Haplotype'] = main_df['Sample_Haplotype'].str.replace('h1', 'hap1').str.replace('h2', 'hap2')

# Path to all BED files
bed_files_path = '/home/alextu/scratch/mei_analysis/mei_hap_specific_beds_flanks_withdesignations/*.bed'

# Initialize merged_main_df if not already defined
merged_main_df = pd.DataFrame()

# Iterate through each BED file
for bed_file in glob.glob(bed_files_path):
    # Extract the sample identifier (e.g., HG00513.h1) from the filename
    bed_filename = os.path.basename(bed_file)
    bed_sample = bed_filename.split('.')[0] + '_' + bed_filename.split('.')[1]  # e.g., 'HG00513_h1'

    # Replace 'h1' and 'h2' with 'hap1' and 'hap2' for consistency
    bed_sample = bed_sample.replace('h1', 'hap1').replace('h2', 'hap2')
    print(f"\nProcessing BED file: {bed_filename} for sample: {bed_sample}")

    # Load the BED file into a DataFrame
    bed_df = pd.read_csv(bed_file, sep='\t', header=None, 
                         names=['chrom', 'start', 'end', 'identifier', 'ref', 'alt', 'te_designation', 'l1me_aid_info'])

    # Print the first few rows of the BED DataFrame for verification
    print("BED DataFrame sample:\n", bed_df.head())

    # Filter the main DataFrame to only include rows matching the current BED sample
    filtered_main_df = main_df[main_df['Sample_Haplotype'] == bed_sample]
    print("Filtered main DataFrame sample for current BED:\n", filtered_main_df.head())

    # Merge the filtered bed DataFrame with the filtered main DataFrame based on the identifier column
    merged_df = pd.merge(
        filtered_main_df,
        bed_df[['identifier', 'te_designation', 'l1me_aid_info']],
        left_on='Identifier',
        right_on='identifier',
        how='left'
    )

    # Print the merged DataFrame sample to verify that columns were appended correctly
    print("Merged DataFrame sample:\n", merged_df.head())

    # Append the merged data to the new DataFrame and remove duplicates
    merged_main_df = pd.concat([merged_main_df, merged_df], ignore_index=True).drop_duplicates()

# Save the new DataFrame with the merged information to a CSV file
output_file = '/home/alextu/scratch/mei_analysis/MEIflanks_collapsed_summary_metrics_chr_position_with_TE_designations.csv'
merged_main_df[['Sample_Haplotype_Chromosome', 'Motif Type', 'Start', 'End', 'te_designation', 'l1me_aid_info']].to_csv(output_file, index=False)

print("\nUpdated CSV with appended columns has been saved.")