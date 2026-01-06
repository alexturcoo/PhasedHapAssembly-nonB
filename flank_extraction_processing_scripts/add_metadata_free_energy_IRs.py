import pandas as pd
import glob
import os
import re  # Import regex module

# ==============================
# Step 1: Define Paths
# ==============================

# Path to all BED files
bed_files_path = '/home/alextu/scratch/mei_analysis/mei_hap_specific_beds_flanks_withdesignations/*.bed'

# Directory containing the TSV files to annotate
tsv_input_dir = '/home/alextu/scratch/mei_analysis/free_energy_IRs_MEIs/'

# Directory to save the annotated TSV files
tsv_output_dir = '/home/alextu/scratch/mei_analysis/free_energy_IRs_MEIs_annotated/'

# Create the output directory if it doesn't exist
os.makedirs(tsv_output_dir, exist_ok=True)

# ==============================
# Step 2: Iterate Through Each BED File
# ==============================

for bed_file in glob.glob(bed_files_path):
    # Extract the BED filename
    bed_filename = os.path.basename(bed_file)
    
    # Example BED filename: 'HG01596.h2.MEIcoords2000flank_bedtools.bed'
    # Use regex to extract 'HG01596' and 'h2'
    match = re.match(r'^(HG\d+)\.h([12])\..*\.bed$', bed_filename)
    
    if match:
        hg_number = match.group(1)  # 'HG01596'
        hap_number = match.group(2)  # '2'
        bed_sample = f"{hg_number}_hap{hap_number}"  # 'HG01596_hap2'
    else:
        print(f"\nUnexpected BED filename format: '{bed_filename}'. Skipping this file.\n")
        continue  # Skip files that do not match the expected pattern
    
    print(f"\nProcessing BED file: '{bed_filename}' for sample: '{bed_sample}'")
    
    # ==============================
    # Step 3: Load the BED File
    # ==============================
    
    try:
        # Load the BED file into a DataFrame
        bed_df = pd.read_csv(
            bed_file, 
            sep='\t', 
            header=None, 
            names=['chrom', 'start', 'end', 'identifier', 'ref', 'alt', 'te_designation', 'l1me_aid_info']
        )
        print("BED DataFrame loaded successfully. Sample data:")
        print(bed_df.head(), "\n")
    except Exception as e:
        print(f"Error reading BED file '{bed_filename}': {e}. Skipping this file.\n")
        continue  # Skip to the next BED file if there's an error
    
    # ==============================
    # Step 4: Locate the Corresponding TSV File
    # ==============================
    
    # Construct the expected TSV filename based on bed_sample
    # Expected TSV filename format: 'flanking_sequences_HG01596_hap2_IR_free_energy.tsv'
    tsv_filename = f"flanking_sequences_{bed_sample}_IR_free_energy.tsv"
    tsv_path = os.path.join(tsv_input_dir, tsv_filename)
    
    # Check if the corresponding TSV file exists
    if not os.path.exists(tsv_path):
        print(f"Corresponding TSV file '{tsv_filename}' not found for BED file '{bed_filename}'. Skipping.\n")
        continue  # Skip to the next BED file if TSV is not found
    
    print(f"Found corresponding TSV file: '{tsv_filename}'")
    
    # ==============================
    # Step 5: Load the TSV File
    # ==============================
    
    try:
        # Load the TSV file into a DataFrame
        tsv_df = pd.read_csv(tsv_path, sep='\t')
        print("TSV DataFrame loaded successfully. Sample data:")
        print(tsv_df.head(), "\n")
    except Exception as e:
        print(f"Error reading TSV file '{tsv_filename}': {e}. Skipping this file.\n")
        continue  # Skip to the next BED file if there's an error
    
    # ==============================
    # Step 6: Extract 'identifier' from 'Sequence_name'
    # ==============================
    
    # The 'Sequence_name' format: 'chr1:6326452-6328451|chr1_6326451_176_INS|post_flank'
    # We need to extract 'chr1_6326451_176_INS' as 'identifier' to match with BED
    tsv_df['identifier'] = tsv_df['Sequence_name'].apply(lambda x: x.split('|')[1] if '|' in x else None)
    
    # Verify if 'identifier' was extracted correctly
    if tsv_df['identifier'].isnull().any():
        print(f"Warning: Some 'Sequence_name' entries in '{tsv_filename}' do not contain '|'. These rows will have NaN 'identifier'.")
    
    # ==============================
    # Step 7: Merge TSV with BED Data
    # ==============================
    
    # Perform the merge based on 'identifier'
    merged_df = pd.merge(
        tsv_df,
        bed_df[['identifier', 'te_designation', 'l1me_aid_info']],
        on='identifier',
        how='left'
    )
    
    # Check if merge was successful
    if merged_df[['te_designation', 'l1me_aid_info']].isnull().all().all():
        print(f"Warning: No matches found during merge for '{tsv_filename}'. Check the 'identifier' fields.\n")
    else:
        print("Merge completed successfully. Annotated DataFrame sample:")
        print(merged_df.head(), "\n")
    
    # ==============================
    # Step 8: Save the Annotated TSV
    # ==============================
    
    # Define the output TSV path
    annotated_tsv_path = os.path.join(tsv_output_dir, tsv_filename)
    
    try:
        # Save the annotated DataFrame to the output directory
        merged_df.to_csv(annotated_tsv_path, sep='\t', index=False)
        print(f"Annotated TSV saved to: '{annotated_tsv_path}'\n")
    except Exception as e:
        print(f"Error saving annotated TSV '{tsv_filename}': {e}. Skipping this file.\n")

print("\nAll BED files have been processed and corresponding TSVs annotated.\n")