import csv
import os

# Function to parse a single file and return extracted rows
def parse_single_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    rows = []
    current_sample = None

    for line in lines:
        if line.startswith("### Results from"):
            # Extract sample name
            current_sample = line.strip().replace("### Results from ", "")
        elif line.startswith("DATA:"):
            # Extract data row
            data = line.strip().replace("DATA: ", "").split()
            if not all(value == "NA" for value in data):  # Exclude only if ALL values are NA
                rows.append([current_sample] + data)
    return rows

# Function to iterate over a directory and combine all results into a single CSV
def parse_directory(input_dir, output_csv):
    combined_rows = []

    # Iterate over all files in the directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".txt"):  # Process only .txt files
            file_path = os.path.join(input_dir, file_name)
            combined_rows.extend(parse_single_file(file_path))

    # Write all results to a single CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Sample", "POS", "STR", "L", "Q", "SEQUENCE"])
        writer.writerows(combined_rows)

# Example usage
parse_directory('/home/alextu/scratch/extract_sv_flanks_2000bp/annotated_flanks_quadron/', 'all_combined_quadron_results_SV_flanks.csv')