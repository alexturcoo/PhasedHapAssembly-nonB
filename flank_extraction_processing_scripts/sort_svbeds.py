import pandas as pd
import os
import glob

# Define the directory containing the BED files
input_dir = "/home/alextu/projects/def-sushant/verkko_batch123_nonB_annotations_aligned_july2024/SVcoords/"
output_dir = "/home/alextu/projects/def-sushant/verkko_batch123_nonB_annotations_aligned_july2024/SVcoords_sorted/"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get a list of all BED files in the input directory
bed_files = glob.glob(os.path.join(input_dir, "*.bed"))

# Loop through each BED file and sort it
for bed_file in bed_files:
    # Get the file name from the path
    file_name = os.path.basename(bed_file)

    # Define the output path for the sorted BED file
    output_bed_file = os.path.join(output_dir, file_name)

    # Read the BED file into a pandas DataFrame
    columns = ["chr", "start", "end", "id", "sequence", "alt"]  # Adjust column names if needed
    df = pd.read_csv(bed_file, sep='\t', header=None, names=columns)

    # Sort first by 'id' (4th column), then by 'start' (2nd column)
    sorted_df = df.sort_values(by=["id", "start"])

    # Write the sorted DataFrame back to a new BED file
    sorted_df.to_csv(output_bed_file, sep='\t', index=False, header=False)

    print(f"Sorted BED file saved as {output_bed_file}")