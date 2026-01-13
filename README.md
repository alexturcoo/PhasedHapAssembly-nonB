# PhasedHapAssembly-nonB
Non-B DNA motif annotation across 65 high quality phased haplotype assemblies.

# Haplotype Assembly Data Utilized for annotations

| Annotation Tool | Alignment Reference | Batch                    | Number of Haplotypes |
|-----------------|---------------------|--------------------------|----------------------|
| nBMST & Quadron | CHM13v2.0 & GRCh38  | 20230818_verkko_batch1   | 76                   |          
| nBMST & Quadron | CHM13v2.0 & GRCh38  | 20230927_verkko_batch2   | 30                   |          
| nBMST & Quadron | CHM13v2.0 & GRCh38  | 20240201_verkko_batch3   | 24                   |                  
| **Total**       |                     |                          | **130**   |          

# analysis_scripts
1. `all_analysis_notebooks` - Contains Jupyter Notebooks (.ipynb) related to all analyses performed over the course of this project
2. `CDKN1A_cruciform_analysis` - Code and associated files used to produce data pertaining to the CDKN1A inverted repeat stability analysis
3. `flanking_sv_mei_analysis` - Code to create density plots for non-B DNA motifs located in the flanking regions around structural variant breakpoints.

# annotation_scripts_wholegenome
Scripts related to annotating and formatting haplotype level fasta files with non-B gfa and Quadron tools. Most scripts were built for running on high performance computing clusters as they utilize array jobs to speed up the processing time of individual haplotype.

# centromere_processing_scripts
Scripts related to annotating non-B DNA structures in completely assembled centromeres using non-B gfa and Quadron tools. Most scripts were built for running on high performance computing clusters as they utilize array jobs to speed up the processing time of individual haplotype.

# flank_extraction_processing_scripts
Scripts related to extracting 2000bp flanks surrounding structural variants (SVs) and mobile element insertions (MEIs) from individual haplotypes. 

# IR_free_energy_processing_seqfold
Scripts related to obtaining free energy prediction for IRs using Seqfold tool.

# main_figures_and_supplementary_notebooks
1. `HGSVC_nonB_figures.ipynb` - Contains Jupyter Notebooks (.ipynb) related to analyses that made it into the main paper.
2. `HGSVC_nonB_supplementary_figures` - Contains Jupyter Notebooks (.ipynb) related to analyses that made it into the Supplementaries.

# preprocessing_aligned_assemblies
Scripts used to preprocess Verkko Phased Haplotype Assemblies (Batch 1,2,3) aligned to both T2T-CHM13v2.0 and GRCh38 at the WHOLE GENOME LEVEL
1. `phased_haplotype_alignments_20230818_verkko_batch1.sh` - Script to take phased haplotype assemblies (BAM files) aligned to reference (chm13 or hg38), filter alignments to obtain ONLY primary reads, then split the bam file by chromosome and write each chromosome bam to a fasta file

