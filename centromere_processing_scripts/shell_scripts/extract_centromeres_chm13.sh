#!/bin/bash
#SBATCH --account=def-sushant
#SBATCH --nodes=1 # specify number of gpus
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G # MEMORY PER NODE
#SBATCH --time=1:00:00 # hrs:mins:secs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alexanderturco1@gmail.com # sends me an email once done
#SBATCH --job-name=extract_centromeres_chm13
#SBATCH --output=extract_centromeres_chm13.o
#SBATCH --error=extract_centromeres_chm13.e

module load samtools

# Define the path to your CHM13 fasta file
CHM13_FASTA="/home/alextu/scratch/reference_genomes/ref_genome_chm13_hprc/chm13v2.0.fa"

# Create an output directory for intermediate files
mkdir -p /home/alextu/scratch/centromere_analysis/centromeres_extracted

# Extract the centromere regions using the start and end positions
samtools faidx $CHM13_FASTA chr1:121796048-126300487 > centromeres_extracted/chr1_121796048_126300487.fasta
samtools faidx $CHM13_FASTA chr10:39633793-41664589 > centromeres_extracted/chr10_39633793_41664589.fasta
samtools faidx $CHM13_FASTA chr11:51035789-54450838 > centromeres_extracted/chr11_51035789_54450838.fasta
samtools faidx $CHM13_FASTA chr12:34620838-37202490 > centromeres_extracted/chr12_34620838_37202490.fasta
samtools faidx $CHM13_FASTA chr13:15547593-17498291 > centromeres_extracted/chr13_15547593_17498291.fasta
samtools faidx $CHM13_FASTA chr14:10092112-12708411 > centromeres_extracted/chr14_10092112_12708411.fasta
samtools faidx $CHM13_FASTA chr15:16678794-17694466 > centromeres_extracted/chr15_16678794_17694466.fasta
samtools faidx $CHM13_FASTA chr16:35848286-37829521 > centromeres_extracted/chr16_35848286_37829521.fasta
samtools faidx $CHM13_FASTA chr17:23892419-27486939 > centromeres_extracted/chr17_23892419_27486939.fasta
samtools faidx $CHM13_FASTA chr18:15965699-20933550 > centromeres_extracted/chr18_15965699_20933550.fasta
samtools faidx $CHM13_FASTA chr19:25817676-29768171 > centromeres_extracted/chr19_25817676_29768171.fasta
samtools faidx $CHM13_FASTA chr2:92333543-94673023 > centromeres_extracted/chr2_92333543_94673023.fasta
samtools faidx $CHM13_FASTA chr20:26925852-29099655 > centromeres_extracted/chr20_26925852_29099655.fasta
samtools faidx $CHM13_FASTA chr21:10962853-11306205 > centromeres_extracted/chr21_10962853_11306205.fasta
samtools faidx $CHM13_FASTA chr22:12788180-15711065 > centromeres_extracted/chr22_12788180_15711065.fasta
samtools faidx $CHM13_FASTA chr3:91738002-96415026 > centromeres_extracted/chr3_91738002_96415026.fasta
samtools faidx $CHM13_FASTA chr4:49705154-55199795 > centromeres_extracted/chr4_49705154_55199795.fasta
samtools faidx $CHM13_FASTA chr5:47039134-49596625 > centromeres_extracted/chr5_47039134_49596625.fasta
samtools faidx $CHM13_FASTA chr6:58286706-61058390 > centromeres_extracted/chr6_58286706_61058390.fasta
samtools faidx $CHM13_FASTA chr7:60414372-63714499 > centromeres_extracted/chr7_60414372_63714499.fasta
samtools faidx $CHM13_FASTA chr8:44215832-46325080 > centromeres_extracted/chr8_44215832_46325080.fasta
samtools faidx $CHM13_FASTA chr9:44951775-47582595 > centromeres_extracted/chr9_44951775_47582595.fasta
samtools faidx $CHM13_FASTA chrX:57820107-60927025 > centromeres_extracted/chrX_57820107_60927025.fasta
samtools faidx $CHM13_FASTA chrY:10565750-10883085 > centromeres_extracted/chrY_10565750_10883085.fasta

# Concatenate the extracted regions into a single fasta file with appropriate headers
cat centromeres_extracted/*.fasta | sed 's/>.*/&/' > centromeres_extracted/all_centromere_regions.fasta

# The final fasta file with all the centromere regions
echo "All centromere regions have been extracted to: centromeres_extracted/all_centromere_regions.fasta"
