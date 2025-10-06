import pandas as pd
import glob
import os

# === Region Settings ===
target_chr = "chr6"
target_start = 36675000
target_end = 36682000

# === Annotation File ===
annotation_file = "/home/alextu/projects/def-sushant/alextu/PhasedHapAssembly-nonB/analysis_scripts/Biological regions  aggregate  NCBI RefSeq Annotation GCF_000001405.40-RS_2024_08.BED"
annotations = pd.read_csv(annotation_file, sep="\t", header=None,
                          names=["chrom", "start", "end", "feature", "score", "strand"])

# === Filter relevant annotations
annotations = annotations[
    (annotations["chrom"] == "NC_000006.12") &
    (annotations["end"] >= target_start) &
    (annotations["start"] <= target_end) &
    (annotations["feature"].isin(["pELS", "PLS", "exon1"]))
].copy()

# === Convert NC_000006.12 to chr6
annotations["chrom"] = "chr6"

# === Export annotations for R (BED format)
annotations[["chrom", "start", "end", "feature"]].to_csv("P21_annotations.bed", sep="\t", header=False, index=False)

# === IR File Processing ===
all_files = sorted(glob.glob("/home/alextu/scratch/free_energy_IRs_verkko_123_wholegenome_hg38/*_IR_free_energy.tsv"))[:123]

midpoints = []
weights = []

for file in all_files:
    print(f"Processing {file}")
    df = pd.read_csv(file, sep="\t")
    df["chrom"] = df["Sequence_name"].str.extract(r"\|(chr\d+)")
    df = df[
        (df["chrom"] == target_chr) &
        (df["Start"] >= target_start) &
        (df["Stop"] <= target_end)
    ]

    if not df.empty:
        mids = ((df["Start"] + df["Stop"]) // 2).tolist()
        fe_values = df["Free_Energy"].tolist()

        midpoints.extend(mids)
        weights.extend([abs(fe) for fe in fe_values])  # positive weights

# === Build BED format for midpoints + weights
ir_df = pd.DataFrame({
    "chr": [target_chr] * len(midpoints),
    "start": midpoints,
    "end": [x + 1 for x in midpoints],  # point representation
    "weight": weights
})

# === Export IR midpoints for R (BED format with weights in 4th column)
ir_df.to_csv("IR_midpoints_weighted.bed", sep="\t", header=False, index=False)