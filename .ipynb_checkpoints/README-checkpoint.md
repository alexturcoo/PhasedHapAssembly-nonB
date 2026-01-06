# PhasedHapAssembly-nonB
Non-B DNA motif annotation across high quality phased haplotype assemblies

# Haplotype Assembly Data Utilized for annotations

| Annotation Tool | Alignment Reference | Batch                    | Number of Haplotypes |
|-----------------|---------------------|--------------------------|----------------------|
| nBMST           | chm13               | 20230818_verkko_batch1   | 76                   |          
| nBMST           | chm13               | 20230927_verkko_batch2   | 30                   |          
| nBMST           | chm13               | 20240201_verkko_batch3   | 24                   |          
| **Total**       |                     |                          | **130**              |          
| nBMST           | hg38                | 20230818_verkko_batch1   | 76                   |          
| nBMST           | hg38                | 20230927_verkko_batch2   | 30                   |          
| nBMST           | hg38                | 20240201_verkko_batch3   | 24                   |          
| **Total**       |                     |                          | **130**              |          
| Quadron         | chm13               | 20230818_verkko_batch1   | 76                   |          
| Quadron         | chm13               | 20230927_verkko_batch2   | 30                   |          
| Quadron         | chm13               | 20240201_verkko_batch3   | 24                   |         
| **Total**       |                     |                          | **130**              |          
| Quadron         | hg38                | 20230818_verkko_batch1   | 76                   |          
| Quadron         | hg38                | 20230927_verkko_batch2   | 30                   |          
| Quadron         | hg38                | 20240201_verkko_batch3   | 24                   |          
| **Total**       |                     |                          | **130**              |          

# Analysis Scripts
1. `centromere_analysis.ipynb` - Notebook containing python analysis of centromere annotations across phased haplotype assemblies
2. `centromere_analysis_active_asat_hor_arrays.ipynb` - Notebook containing python anlysis of active alpha satellite HOR arrays within phased haplotype chromosomes
3. `examine_nonb_annotations_chm13.ipynb` - Older notebook containing python analysis of Phased Haplotype assembly non-b motif annotations across whole genome
4. `hgsvc_phased_haplotype_analysis_final.ipynb` - Newer notebook containing python analysis of Phased Haplotype Assembly non-b motif annotations across whole genome
5. `rdna_analysis.ipynb` - Notebook containing python analysis of ribosomeal DNA arrays across phased haplotype assemblies
6. `shared_nonB_motifs_analysis.ipynb` - Notebook containing python analysis of shared non-B DNA motifs across haplotypes
7. `sv_flank_extraction.ipynb` - Notebook containing python test code to extract flanking regions of SVs and MEIs

# preprocessing_scripts_wholegenome
Scripts used to preprocess Verkko Phased Haplotype Assemblies (Batch 1,2,3) aligned to both T2T-CHM13v2.0 and GRCh38 at the WHOLE GENOME LEVEL
1. `phased_haplotype_alignments_20230818_verkko_batch1.sh` - Script to take phased haplotype assemblies (BAM files) aligned to reference (chm13 or hg38), filter alignments to obtain ONLY primary reads, then split the bam file by chromosome and write each chromosome bam to a fasta file

# annotation_scripts_wholegenome
Scripts used to annotate Verkko Phased Haplotype Assemblies (Batch 1,2,3) aligned to both T2T-CHM13v2.0 and GRCh38 at the WHOLE GENOME LEVEL

### nBMST ANNOTATION PROCESSING
1. `find_nonb_motifs_haplotype_array.sh` - Script to annotate phased haplotype assemblies (alignments) using the non-b gfa tool (nBMST)
2. `nonoverlapping_motifs.sh` - Script to merge/collapse overlapping intervals for specific non-B motif annotations from non-B motif search tool (nBMST) (outputs collapsed bed file for each specific motif type from nBMST)
3. `process_bed_files.py` - Script to process collapsed bed files from nBMST and obtain metrics such as Motif Counts, Bases Covered by Motif, and Percentage of Genome covered by motif for each haplotype.
4. `process_bed_files.sh` - Associated shell script to run the python script
### QUADRON ANNOTATION PROCESSING
5. `run_quadron.sh` - Script to annotate phased haplotype assemblies (alignments) using quadron
6. `run_quadron_haplotigs.sh` - Script to annotate phased haplotype assemblies (haplotigs) using quadron
7. `process_quadron_files.py` - Script to process .txt output from Quadron and format into dataframes with stability score greater than 19
8. `process_quadron_files.sh` - Associated shell script to run the python script
9. `quadron_to_bed.py` - Script to format quadron dataframes (Q > 19) into bed files, collapses annotations, and splits bed files based on G quadruplex Strand
10. `quadron_to_bed.sh` - Associated shell script to run the python script
11. `process_gquad_beds_quadron.py` - Script to process collapsed bed files from Quadron and obtain metrics of G-quadruplex (Motif Counts, Bases Covered by Motif, and Percentage of Genome covered) for each haplotype
12. `process_gquad_beds_quadron.sh` - Associated shell script to run the python script
### EXTRAS
13. `bedtools_intersect.sh` - Intersect all haplotypes with reference and find common regions across motifs

# centromere_scripts
Scripts used to annotate centromeres in both reference genomes (GRCh38 and CHM13-T2T) AND Verkko Phased Haplotype Assemblies (Batch 1,2,3)



# rDNA_scripts
Scripts used to annotate Verkko Phased Haplotype Assemblies (Batch 1,2,3) aligned to only T2T-CHM13v2.0 (rDNA arrays unavailable for GRCh38)
1. `phased_haplotype_alignments_20230818_verkko_batch1.sh` - Script to take phased haplotype rDNA arrays (Bam files) aligned to chm13v2.0, filter alignments to obtain ONLY primary reads, then split the bam file by chromosome and write each chromosome bam to a fasta file
2. 
3. 
4.
