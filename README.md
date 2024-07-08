# PhasedHapAssembly-nonB
Non-B DNA motif annotation across high quality phased haplotype assemblies

# Haplotype Assembly Data Utilized for annotations

| Annotation Tool | Alignment Reference | Batch                    | Number of Haplotypes | Location |
|-----------------|---------------------|--------------------------|----------------------|----------|
| nBMST           | chm13               | 20230818_verkko_batch1   | 76                   |          |
| nBMST           | chm13               | 20230927_verkko_batch2   | 30                   |          |
| nBMST           | chm13               | 20240201_verkko_batch3   | 24                   |          |
| **Total**       |                     |                          | **130**              |          |
| nBMST           | hg38                | 20230818_verkko_batch1   | 76                   |          |
| nBMST           | hg38                | 20230927_verkko_batch2   | 30                   |          |
| nBMST           | hg38                | 20240201_verkko_batch3   | 24                   |          |
| **Total**       |                     |                          | **130**              |          |
| Quadron         | chm13               | 20230818_verkko_batch1   | 76                   |          |
| Quadron         | chm13               | 20230927_verkko_batch2   | 30                   |          |
| Quadron         | chm13               | 20240201_verkko_batch3   | 24                   |          |
| **Total**       |                     |                          | **130**              |          |
| Quadron         | hg38                | 20230818_verkko_batch1   | 76                   |          |
| Quadron         | hg38                | 20230927_verkko_batch2   | 30                   |          |
| Quadron         | hg38                | 20240201_verkko_batch3   | 24                   |          |
| **Total**       |                     |                          | **130**              |          |

# preprocessing_scripts
1. `phased_haplotype_alignments_20230818_verkko_batch1.sh` - Script to take phased haplotype assemblies (BAM files) aligned to reference (chm13 or hg38), filter alignments to obtain ONLY primary reads, then split the bam file by chromosome and write each chromosome bam to a fasta file
2. `nonoverlapping_motifs.sh` - Script to merge/collapse overlapping intervals for specific non-B motif annotations from non-B motif search tool (nBMST) (outputs collapsed bed file for each specific motif type from nBMST)

# annotation_scripts
1. `process_bed_files.py` - Script to process collapsed bed files from nBMST and obtain metrics such as Motif Counts, Bases Covered by Motif, and Percentage of Genome covered by motif for each haplotype.
2. `process_bed_files.sh` - Associated shell script to run the python script
3. `process_quadron_files.py` - Script to process .txt output from Quadron and format into dataframes with stability score greater than 19
4. `process_quadron_files.sh` - Associated shell script to run the python script
5. `quadron_to_bed.py` - Script to format quadron dataframes (Q > 19) into bed files, collapses annotations, and splits bed files based on G quadruplex Strand
6. `quadron_to_bed.sh` - Associated shell script to run the python script
7. `process_gquad_beds_quadron.py` - Script to process collapsed bed files from Quadron and obtain metrics of G-quadruplex (Motif Counts, Bases Covered by Motif, and Percentage of Genome covered) for each haplotype
8. `process_gquad_beds_quadron.sh` - Associated shell script to run the python script

# Analysis Scripts
1. `examine_nonb_annoations.ipynb` - A jupyter notebook with analysis of Phased Haplotype assembly non-b motif annotations
