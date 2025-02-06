import os
import pandas as pd
from seqfold import dg
from concurrent.futures import ProcessPoolExecutor

# ==========================
# Configuration
# ==========================
INPUT_FILE = "/home/alextu/scratch/extract_sv_flanks_2000bp/annotated_flanks_nbmst/flanking_sequences_HG00096_hap1/flanking_sequences_HG00096_hap1_IR.tsv"
OUTPUT_FOLDER = "/home/alextu/scratch/extract_sv_flanks_2000bp/free_energy_IRs"
NUM_CORES = 32  # Adjust cores as needed

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================
# Function to Calculate Free Energy
# ==========================
def calculate_free_energy(sequence):
    """
    Calculates the free energy for a given sequence using the seqfold library.
    Returns the free energy value as a float.
    """
    try:
        return dg(sequence, temp=37.0)  # Temperature in Celsius
    except Exception as e:
        print(f"Error calculating free energy for sequence: {sequence}\n{e}")
        return None

# ==========================
# Parallel Processing
# ==========================
def parallel_apply(df, func, column, cores=NUM_CORES):
    """
    Apply a function to a column in a pandas DataFrame using parallel processing.
    """
    with ProcessPoolExecutor(max_workers=cores) as executor:
        results = list(executor.map(func, df[column]))
    return results

# ==========================
# Main Processing
# ==========================
def process_file(input_file, output_folder):
    # Load the input TSV
    df = pd.read_csv(input_file, sep="\t")

    # Check for required columns
    required_columns = ["Sequence_name", "Start", "Stop", "Length", "Sequence"]
    if not all(col in df.columns for col in required_columns):
        print(f"Error: Input file does not contain all required columns: {required_columns}")
        return

    # Calculate free energy in parallel for all rows
    print("Calculating free energies for sequences...")
    df["Free_Energy"] = parallel_apply(df, calculate_free_energy, "Sequence")

    # Select only the desired columns
    df = df[["Sequence_name", "Start", "Stop", "Length", "Sequence", "Free_Energy"]]

    # Build output filename
    base_name = os.path.basename(input_file)
    new_file_name = base_name.replace(".tsv", "_free_energy.tsv")
    output_file = os.path.join(output_folder, new_file_name)

    # Save the DataFrame
    df.to_csv(output_file, sep="\t", index=False)
    print(f"Processed file saved to: {output_file}")

# Run the script
process_file(INPUT_FILE, OUTPUT_FOLDER)