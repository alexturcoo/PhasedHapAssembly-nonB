import os
import pandas as pd
from seqfold import dg
from concurrent.futures import ProcessPoolExecutor

# Configuration
INPUT_FILE = "/home/alextu/scratch/annotated_flanks_nbmst/flanking_sequences_HG00096_hap1/flanking_sequences_HG00096_hap1_IR.tsv"
OUTPUT_FOLDER = "/home/alextu/scratch/free_energy_IRs"
NUM_CORES = 32  # Adjust cores as needed

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def calculate_free_energy(sequence):
    try:
        return dg(sequence, temp=37.0)
    except Exception as e:
        print(f"Error for sequence: {sequence[:10]}... {e}")
        return None

def process_chunk(chunk):
    # Calculate free energy for each sequence in the chunk
    chunk["Free_Energy"] = chunk["Sequence"].apply(calculate_free_energy)
    return chunk

def process_file_in_chunks(input_file, output_folder, num_cores=NUM_CORES, chunk_size=1000):
    # Load full DataFrame
    df = pd.read_csv(input_file, sep="\t")
    required_columns = ["Sequence_name", "Start", "Stop", "Length", "Sequence"]
    if not all(col in df.columns for col in required_columns):
        print(f"Error: Missing required columns.")
        return

    # Split DataFrame into chunks
    chunks = [df.iloc[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
    
    # Process each chunk in parallel
    processed_chunks = []
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        for processed_chunk in executor.map(process_chunk, chunks):
            processed_chunks.append(processed_chunk)
    
    # Concatenate all processed chunks
    result_df = pd.concat(processed_chunks)
    
    # Keep desired columns and save to file
    result_df = result_df[["Sequence_name", "Start", "Stop", "Length", "Sequence", "Free_Energy"]]
    base_name = os.path.basename(input_file)
    output_file = os.path.join(output_folder, base_name.replace(".tsv", "_free_energy.tsv"))
    result_df.to_csv(output_file, sep="\t", index=False)
    print(f"Processed file saved to: {output_file}")

# Run processing
process_file_in_chunks(INPUT_FILE, OUTPUT_FOLDER)
