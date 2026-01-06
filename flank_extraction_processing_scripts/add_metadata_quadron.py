import pandas as pd
import glob
import os

# Load the main CSV file
main_df = pd.read_csv('/home/alextu/scratch/mei_analysis/all_combined_quadron_results_MEI_flanks.csv')  # Replace with your new main CSV file path

# Remove the "flanking_sequences_" prefix from the 'Sample' column
main_df['Sample_Clean'] = main_df['Sample'].str.replace('flanking_sequences_', '')

# Extract the correct unique identifier
# Extracts e.g., chr10_100876072_324_INS
def extract_identifier(sample):
    parts = sample.split('_')
    return f"{parts[4]}_{parts[5]}_{parts[6]}_{parts[7]}"

main_df['Identifier'] = main_df['Sample_Clean'].apply(extract_identifier)

# Print the first few Identifier values for verification
print("\nIdentifiers extracted from the main CSV file:")
print(main_df[['Sample', 'Identifier']].head())

# Normalize the haplotype naming convention to match BED files (hap1 -> h1, hap2 -> h2)
main_df['Sample_Haplotype'] = main_df['Sample_Clean'].apply(lambda x: x.split('_')[0] + '_' + x.split('_')[1])  # e.g., HG00733_hap2
main_df['Sample_Haplotype'] = main_df['Sample_Haplotype'].str.replace('hap1', 'h1').str.replace('hap2', 'h2')  # Normalize to h1/h2

# Print the first few Sample_Haplotype values for verification
print("\nSample Haplotypes extracted from the main CSV file:")
print(main_df[['Sample', 'Sample_Haplotype']].head())

# Path to all BED files
bed_files_path = '/home/alextu/scratch/mei_analysis/mei_hap_specific_beds_flanks_withdesignations/*.bed'  # Replace with your actual BED files path

# Initialize merged_main_df
merged_main_df = pd.DataFrame()

# Iterate through each BED file
for bed_file in glob.glob(bed_files_path):
    # Extract the sample identifier (e.g., HG00733_h2) from the filename
    bed_filename = os.path.basename(bed_file)
    bed_sample = bed_filename.split('.')[0] + '_' + bed_filename.split('.')[1]  # e.g., 'HG00733_h2'

    print(f"\nProcessing BED file: {bed_filename} for sample: {bed_sample}")

    # Load the BED file into a DataFrame
    bed_df = pd.read_csv(bed_file, sep='\t', header=None, 
                         names=['chrom', 'start', 'end', 'identifier', 'ref', 'alt', 'te_designation', 'l1me_aid_info'])

    # Print the first few rows of the BED DataFrame for verification
    print("\nBED DataFrame sample:\n", bed_df.head())

    # Filter the main DataFrame to only include rows matching the current BED sample
    filtered_main_df = main_df[main_df['Sample_Haplotype'] == bed_sample]
    print("\nFiltered main DataFrame for current BED sample:")
    print(filtered_main_df[['Sample', 'Identifier', 'Sample_Haplotype']].head())

    # Merge the filtered bed DataFrame with the filtered main DataFrame based on the identifier column
    merged_df = pd.merge(
        filtered_main_df,
        bed_df[['identifier', 'te_designation', 'l1me_aid_info']],
        left_on='Identifier',
        right_on='identifier',
        how='left'
    )

    # Print the merged DataFrame sample to verify that columns were appended correctly
    print("\nMerged DataFrame sample:")
    print(merged_df[['Sample', 'Identifier', 'te_designation', 'l1me_aid_info']].head())

    # Append the merged data to the new DataFrame and remove duplicates
    merged_main_df = pd.concat([merged_main_df, merged_df], ignore_index=True).drop_duplicates()

# Save the new DataFrame with the merged information to a CSV file
output_file = '/home/alextu/scratch/mei_analysis/all_combined_quadron_results_MEI_flanks_with_TE_designations.csv'  # Replace with your desired output path
merged_main_df[['Sample', 'POS', 'STR', 'L', 'Q', 'SEQUENCE', 'te_designation', 'l1me_aid_info']].to_csv(output_file, index=False)

print("\nUpdated CSV with appended columns has been saved.")