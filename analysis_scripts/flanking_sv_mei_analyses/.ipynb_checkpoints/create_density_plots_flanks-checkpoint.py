import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import sys

# DENSITY PLOTS FOR NON-B DNA MOTIFS AROUND SV (INS AND DEL) BREAKPOINTS 2000bp UP AND DOWNSTREAM

# ==========================
# Configuration
# ==========================
DEBUG = True  # Set to False to disable debug print statements

# File paths
SV_FILE_PATH = '/home/alextu/projects/def-sushant/alextu/extract_SV_and_MEI_flank_scripts/SVflanks_collapsed_summary_metrics_chr_position.csv'
G4_FILE_PATH = '/home/alextu/projects/def-sushant/alextu/extract_SV_and_MEI_flank_scripts/all_combined_quadron_results_SV_flanks.csv'

# Plot configurations
PLOT_SIZE = (10, 6)
X_LIMITS = (-2000, 2000)
PLOT_SAVE_DIR = '/home/alextu/projects/def-sushant/'  # Update as needed

# ==========================
# Utility Functions
# ==========================
def debug_print(*args):
    """Utility function for conditional debugging."""
    if DEBUG:
        print(*args)

# ==========================
# 1. Load the CSV Data
# ==========================
def load_csv(file_path, description):
    """Load a CSV file and handle errors."""
    debug_print(f"Loading {description} from '{file_path}'...")
    try:
        df = pd.read_csv(file_path)
        debug_print(f"Successfully loaded {description}. Shape: {df.shape}")
        debug_print(f"{description} Data Sample:")
        debug_print(df.head())
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print(f"Error: The file '{file_path}' does not appear to be in CSV format or is malformed.")
        sys.exit(1)

df_sv = load_csv(SV_FILE_PATH, "SV data")
df_g4 = load_csv(G4_FILE_PATH, "G4 data")

# ==========================
# 2. Process SV Data
# ==========================
def process_sv_data(df):
    """
    Process the SV DataFrame to extract sv_type, haplotype, flank, and calculate relative positions.
    Utilizes vectorized operations for efficiency.
    """
    debug_print("\nProcessing SV data...")

    # Compile regex pattern
    sv_pattern = re.compile(r'hap(\d+)\|.*_(INS|DEL)\|(pre|post)_flank')

    # Extract sv_type, haplotype, and flank using vectorized str.extract
    extraction = df['Sample_Haplotype_Chromosome'].str.extract(sv_pattern)
    extraction.columns = ['haplotype_num', 'sv_type', 'flank']
    debug_print("After extracting haplotype_num, sv_type, and flank:")
    debug_print(extraction.head())

    # Join extraction results with original DataFrame
    df = df.join(extraction)

    # Separate matched and unmatched samples
    matched_sv = df.dropna(subset=['sv_type', 'haplotype_num', 'flank'])
    unmatched_sv = df[df[['sv_type', 'haplotype_num', 'flank']].isnull().any(axis=1)]

    # Print counts
    debug_print(f"Total SV samples: {df.shape[0]}")
    debug_print(f"Matched SV samples: {matched_sv.shape[0]}")
    debug_print(f"Unmatched SV samples: {unmatched_sv.shape[0]}")

    # Print samples
    if not matched_sv.empty:
        debug_print("\nSample of matched SV extractions:")
        debug_print(matched_sv[['Sample_Haplotype_Chromosome', 'sv_type', 'haplotype_num', 'flank']].head())
    else:
        debug_print("\nNo matched SV extractions found.")

    if not unmatched_sv.empty:
        debug_print("\nSample of unmatched SV extractions:")
        debug_print(unmatched_sv[['Sample_Haplotype_Chromosome']].head())
    else:
        debug_print("\nNo unmatched SV extractions found.")

    # Proceed with matched data
    df = matched_sv.copy()

    # Convert haplotype_num to 'hapX' format
    df['haplotype'] = 'hap' + df['haplotype_num'].astype(int).astype(str)
    debug_print("Converted haplotype_num to haplotype:")
    debug_print(df[['haplotype_num', 'haplotype']].head())

    # Calculate relative position
    # For pre flanks: rel_pos = Start - 2000
    # For post flanks: rel_pos = Start
    df['rel_pos'] = df['Start'] - 2000 * (df['flank'] == 'pre')
    debug_print("After calculating rel_pos:")
    debug_print(df[['Start', 'flank', 'rel_pos']].head())

    # Ensure rel_pos is numeric and within expected range
    df['rel_pos'] = pd.to_numeric(df['rel_pos'], errors='coerce')
    df = df[(df['rel_pos'] >= X_LIMITS[0]) & (df['rel_pos'] <= X_LIMITS[1])]
    debug_print(f"SV Data after filtering rel_pos within {X_LIMITS}: {df.shape}")

    # Final SV Data Sample
    debug_print("\nFinal processed SV Data Sample:")
    debug_print(df.head())

    return df

df_sv = process_sv_data(df_sv)

# ==========================
# 3. Process G4 Data
# ==========================
def process_g4_data(df):
    """
    Process the G4 DataFrame to extract sv_type, haplotype, flank, and calculate relative positions.
    Flip rel_pos for pre flanks as per requirement.
    Utilizes vectorized operations for efficiency.
    """
    debug_print("\nProcessing G4 data...")

    # Compile regex pattern
    g4_pattern = re.compile(r'hap(\d+)_.*_(INS|DEL)_(pre|post)_flank\.txt$')

    # Extract sv_type, haplotype, and flank using vectorized str.extract
    extraction = df['Sample'].str.extract(g4_pattern)
    extraction.columns = ['haplotype_num', 'sv_type', 'flank']
    debug_print("After extracting haplotype_num, sv_type, and flank:")
    debug_print(extraction.head())

    # Join extraction results with original DataFrame
    df = df.join(extraction)

    # Separate matched and unmatched samples
    matched_g4 = df.dropna(subset=['sv_type', 'haplotype_num', 'flank'])
    unmatched_g4 = df[df[['sv_type', 'haplotype_num', 'flank']].isnull().any(axis=1)]

    # Print counts
    debug_print(f"Total G4 samples: {df.shape[0]}")
    debug_print(f"Matched G4 samples: {matched_g4.shape[0]}")
    debug_print(f"Unmatched G4 samples: {unmatched_g4.shape[0]}")

    # Print samples
    if not matched_g4.empty:
        debug_print("\nSample of matched G4 extractions:")
        debug_print(matched_g4[['Sample', 'sv_type', 'haplotype_num', 'flank']].head())
    else:
        debug_print("\nNo matched G4 extractions found.")

    if not unmatched_g4.empty:
        debug_print("\nSample of unmatched G4 extractions:")
        debug_print(unmatched_g4[['Sample']].head())
    else:
        debug_print("\nNo unmatched G4 extractions found.")

    # Proceed with matched data
    df = matched_g4.copy()

    # Convert haplotype_num to 'hapX' format
    df['haplotype'] = 'hap' + df['haplotype_num'].astype(int).astype(str)
    debug_print("Converted haplotype_num to haplotype:")
    debug_print(df[['haplotype_num', 'haplotype']].head())

    # Calculate relative position with flipping for pre flanks
    # For pre flanks: rel_pos = POS - 2000
    # For post flanks: rel_pos = POS
    df['rel_pos'] = df['POS'] - 2000 * (df['flank'] == 'pre')  # **Fixed here**
    debug_print("After calculating rel_pos:")
    debug_print(df[['POS', 'flank', 'rel_pos']].head())

    # Ensure rel_pos is numeric and within expected range
    df['rel_pos'] = pd.to_numeric(df['rel_pos'], errors='coerce')
    df = df[(df['rel_pos'] >= X_LIMITS[0]) & (df['rel_pos'] <= X_LIMITS[1])]
    debug_print(f"G4 Data after filtering rel_pos within {X_LIMITS}: {df.shape}")

    # Final G4 Data Sample
    debug_print("\nFinal processed G4 Data Sample:")
    debug_print(df.head())

    return df

df_g4 = process_g4_data(df_g4)

# ==========================
# 4. Generate Density Plots
# ==========================
def plot_density_per_sv_haplotype(df_sv, df_g4, sv_type, haplotype, save_dir=PLOT_SAVE_DIR):
    """
    Plot density for a single SV type and haplotype, including G4 data.
    Utilizes vectorized plotting for efficiency.
    """
    debug_print(f"\nGenerating plot for SV Type: {sv_type}, Haplotype: {haplotype}")

    # Filter data
    df_hap_sv = df_sv[(df_sv['sv_type'] == sv_type) & (df_sv['haplotype'] == haplotype)]
    df_hap_g4 = df_g4[(df_g4['sv_type'] == sv_type) & (df_g4['haplotype'] == haplotype)]

    debug_print(f"SV Data filtered: {df_hap_sv.shape[0]} rows")
    debug_print(f"G4 Data filtered: {df_hap_g4.shape[0]} rows")

    # Check for 'Motif Type' column
    if 'Motif Type' not in df_hap_sv.columns:
        debug_print("Error: 'Motif Type' column not found in SV data.")
        return

    unique_motifs = df_hap_sv['Motif Type'].unique()
    debug_print(f"Unique Motif Types: {unique_motifs}")

    # Assign colors to motifs
    palette = sns.color_palette(n_colors=len(unique_motifs))
    motif_colors = dict(zip(unique_motifs, palette))

    plt.figure(figsize=PLOT_SIZE)

    # Plot motif densities
    if not df_hap_sv.empty:
        debug_print("Plotting SV motif densities...")
        for motif in unique_motifs:
            motif_df = df_hap_sv[df_hap_sv['Motif Type'] == motif]
            if motif_df.empty:
                debug_print(f"No data for motif: {motif}")
                continue
            sns.kdeplot(
                data=motif_df,
                x='rel_pos',
                label=motif,
                linewidth=1.5,
                common_norm=False,
                alpha=0.7,
                color=motif_colors[motif],
                bw_adjust=0.5  # Adjust bandwidth for better fit
            )
    else:
        debug_print("No SV data available for this SV Type and Haplotype.")

    # Plot G4 densities
    if not df_hap_g4.empty:
        debug_print("Plotting G4 densities...")
        sns.kdeplot(
            data=df_hap_g4,
            x=df_hap_g4['rel_pos'] - 1,
            label='G4',
            linewidth=1.5,
            linestyle='-',  # **Changed from '--' to '-'**
            color='green',
            bw_adjust=0.5
        )
    else:
        debug_print("No G4 data available for this SV Type and Haplotype.")

    # Add plot details
    #plt.axvline(0, color='black', linestyle='--', linewidth=1)
    plt.title(f"{sv_type} {haplotype}: Density of Motifs and G4 Relative to Breakpoints", fontsize=16)
    plt.xlabel('Position Relative to SV Breakpoint (bp)', fontsize=14)
    plt.ylabel('Density', fontsize=14)
    plt.xlim(X_LIMITS)
    plt.legend(title='Type', fontsize=10, title_fontsize=12)
    plt.tight_layout()

    # Save plot
    save_path = f"{save_dir}{sv_type}_{haplotype}_density_plot.pdf"
    plt.savefig(save_path, bbox_inches='tight')
    debug_print(f"Plot saved to {save_path}")
    plt.close()

# Define the combinations to plot
sv_haplotype_combinations = [
    ('INS', 'hap1'),
    ('INS', 'hap2'),
    ('DEL', 'hap1'),
    ('DEL', 'hap2')
]

# Generate and save plots for each combination
for sv_type, haplotype in sv_haplotype_combinations:
    plot_density_per_sv_haplotype(
        df_sv, df_g4, sv_type, haplotype
    )

debug_print("\nDensity plots successfully created and saved.")