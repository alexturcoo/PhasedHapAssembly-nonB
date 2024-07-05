# PhasedHapAssembly-nonB
Non-B DNA motif annotation across high quality phased haplotype assemblies

#preprocessing_scripts
1. `phased_haplotype_alignments_20230818_verkko_batch1.sh` - Script to take phased haplotype assemblies (BAM files) aligned to reference (chm13 or hg38), filter alignments to obtain ONLY primary reads, then split the bam file by chromosome and write each chromosome bam to a fasta file
2. `nonoverlapping_motifs.sh` - Script to merge/collapse overlapping intervals for specific non-B motif annotations from non-B motif search tool (nBMST) (outputs collapsed bed file for each specific motif type from nBMST)

#annotation_scripts
1. `process_bed_files.py` - Script to process collapsed bed files from nBMST and obtain metrics such as Motif Counts, Bases Covered by Motif, and Percentage of Genome covered by motif for each haplotype.
2. `process_bed_files.sh` - Associated shell script to run the python script above
3. `process_quadron_files.py` - 
