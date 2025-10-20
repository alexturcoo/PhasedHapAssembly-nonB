import pysam
import os
import sys

def get_sequence_from_bam(bam_file, chrom, start, end):
    bam = pysam.AlignmentFile(bam_file, "rb")
    sequence = []
    current_pos = start

    for pileupcolumn in bam.pileup(chrom, start, end, truncate=True):
        while current_pos < pileupcolumn.pos:
            sequence.append('N')
            current_pos += 1
        
        base_count = {}
        
        for pileupread in pileupcolumn.pileups:
            if pileupread.is_del or pileupread.is_refskip:
                continue
            if pileupread.alignment.mapping_quality < 1:
                continue
            base = pileupread.alignment.query_sequence[pileupread.query_position]
            base_count[base] = base_count.get(base, 0) + 1
        
        if base_count:
            consensus_base = max(base_count, key=base_count.get)
            sequence.append(consensus_base)
        else:
            sequence.append('N')
        
        current_pos = pileupcolumn.pos + 1

    while current_pos <= end:
        sequence.append('N')
        current_pos += 1
    
    bam.close()
    consensus_sequence = ''.join(sequence)
    
    filtered_sequence = consensus_sequence.replace('N', '')
    filtered_length = len(filtered_sequence)
    
    return consensus_sequence, filtered_length, filtered_sequence

def write_fasta(sequence, header, filepath):
    with open(filepath, "w") as fasta_file:
        fasta_file.write(f">{header}\n")
        for i in range(0, len(sequence), 60):
            fasta_file.write(sequence[i:i+60] + "\n")

def process_bam_file(index):
    # Directory containing BAM files
    bam_dir = "/home/alextu/scratch/rdna_analysis/rdna_filtered_chr_bams/chr22"
    # Output directories for FASTA files
    with_Ns_dir = "/home/alextu/scratch/rdna_analysis/rdna_filtered_chr_fasta_2_N/chr22"
    without_Ns_dir = "/home/alextu/scratch/rdna_analysis/rdna_filtered_chr_fasta_2_no_N/chr22"

    os.makedirs(with_Ns_dir, exist_ok=True)
    os.makedirs(without_Ns_dir, exist_ok=True)

    bam_files = sorted([f for f in os.listdir(bam_dir) if f.endswith(".bam")])
    bam_file = bam_files[index]
    bam_path = os.path.join(bam_dir, bam_file)
    
    print(f"Processing {bam_file}...")
    sample_name = os.path.splitext(bam_file)[0]
    chrom = "chr22"  # Assuming the chromosome is always chr14
    start = 4793794  # Start position (adjust if needed)
    end = 5720650    # End position (adjust if needed)

    consensus_sequence, filtered_length, filtered_sequence = get_sequence_from_bam(bam_path, chrom, start, end)
    header = f"{chrom}:{start}-{end}"

    with_Ns_path = os.path.join(with_Ns_dir, f"{sample_name}_with_Ns.fasta")
    without_Ns_path = os.path.join(without_Ns_dir, f"{sample_name}_no_Ns.fasta")

    write_fasta(consensus_sequence, header, with_Ns_path)
    write_fasta(filtered_sequence, header, without_Ns_path)

    print(f"Total length of consensus sequence for {bam_file}: {len(consensus_sequence)}")
    print(f"Length of consensus sequence without 'N's for {bam_file}: {filtered_length}")

if __name__ == "__main__":
    index = int(sys.argv[1])
    process_bam_file(index)
