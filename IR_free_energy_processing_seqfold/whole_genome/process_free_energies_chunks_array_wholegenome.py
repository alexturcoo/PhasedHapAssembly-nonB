import sys
import os
import pandas as pd
from seqfold import dg
from concurrent.futures import ProcessPoolExecutor

# Configuration
NUM_CORES = 32
OUTPUT_FOLDER = "/home/alextu/scratch/free_energy_IRs_verkko_123_wholegenome_chm13"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def calculate_free_energy(sequence):
    """
    Calculates the free energy (kcal/mol) of a nucleotide sequence at 37°C.

    Parameters:
        sequence (str): DNA sequence.

    Returns:
        float: Free energy value, or None if calculation fails.
    """
    try:
        return dg(sequence, temp=37.0)
    except Exception as e:
        print(f"Error for sequence: {sequence[:10]}... {e}")
        return None

def process_chunk(chunk):
    chunk["Free_Energy"] = chunk["Sequence"].apply(calculate_free_energy)
    return chunk

def process_file_in_chunks(input_file, output_folder, num_cores=NUM_CORES, chunk_size=1000):
    """
    Processes a TSV file containing DNA sequences in parallel chunks and calculates their free energy.

    Parameters:
        input_file (str): Path to the input .tsv file with sequence data.
        output_folder (str): Path to the folder where results will be saved.
        num_cores (int): Number of CPU cores to use.
        chunk_size (int): Number of rows per chunk to process.

    Output:
        Writes a new TSV file with calculated free energy per sequence.
    """
    df = pd.read_csv(input_file, sep="\t")
    required_columns = ["Sequence_name", "Start", "Stop", "Length", "Sequence", "Repeat", "Spacer"]
    if not all(col in df.columns for col in required_columns):
        print(f"Error: Missing required columns in {input_file}.")
        return

    chunks = [df.iloc[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
    processed_chunks = []
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        for processed_chunk in executor.map(process_chunk, chunks):
            processed_chunks.append(processed_chunk)

    result_df = pd.concat(processed_chunks)
    result_df = result_df[["Sequence_name", "Start", "Stop", "Length", "Sequence", "Repeat", "Spacer", "Free_Energy"]]
    base_name = os.path.basename(input_file)
    output_file = os.path.join(output_folder, base_name.replace(".tsv", "_free_energy.tsv"))
    result_df.to_csv(output_file, sep="\t", index=False)
    print(f"Processed file saved to: {output_file}")

def main():
    root_folder = "/home/alextu/scratch/home/alextu/scratch/chm13/verkko_batch123_nonb_annotations_aligned_chm13"
    all_files = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for fname in filenames:
            if fname.endswith("_IR.tsv"):
                parent_dir = os.path.basename(dirpath)
                if fname.startswith(parent_dir):
                    all_files.append(os.path.join(dirpath, fname))
    
    try:
        idx = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Please provide a valid task ID.")
        sys.exit(1)

    if idx < 0 or idx >= len(all_files):
        print(f"Index {idx} out of range. Found {len(all_files)} files.")
        sys.exit(1)

    input_file = all_files[idx]
    print(f"Processing file {idx}: {input_file}")
    process_file_in_chunks(input_file, OUTPUT_FOLDER)

if __name__ == "__main__":
    main()
