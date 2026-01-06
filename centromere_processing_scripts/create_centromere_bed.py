#THIS CODE PRODUCES A SINGLE BED FILE THAT BASICALLY SPLITS THE INITIAL FILE PROVIDED BY GLENNIS LOGSDON (ON HGSVC3 FTP SITE AS WELL)
input_file = '/home/alextu/scratch/centromere_analysis/CEN_COORD_UPDATED_Aug7_logsdon/hgsvc3_verkko_v1.4_nonredundant_complete_and_accurate_active_asat_HOR_arrays_v3.list'
output_file = '/home/alextu/scratch/centromere_analysis/CEN_COORD_UPDATED_Aug7_logsdon/hgsvc3_verkko_v1.4_nonredundant_complete_and_accurate_active_asat_HOR_arrays_v3.bed'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        print(line)
        parts = line.strip().split('\t')
        sample_name = parts[0]
        haplotype, positions = parts[1].split(':')
        start, end = positions.split('-')
        chromosome = parts[2]
        
        # Formatting the output line as required
        output_line = f"{haplotype}\t{start}\t{end}\t{sample_name}\t{chromosome}\n"
        outfile.write(output_line)

output_file

#### THIS IS THE CODE WE USE TO PRODUCE INDIVIDUAL BEDS FOR THE HAPLOTYPE CENTROMERES, NOT ABOVE
input_file = '/home/alextu/scratch/centromere_analysis/CEN_COORD_UPDATED_Aug7_logsdon/hgsvc3_verkko_v1.4_nonredundant_complete_and_accurate_active_asat_HOR_arrays_v3.list'

# Dictionary to hold file handles for each haplotype
output_files = {}

try:
    with open(input_file, 'r') as infile:
        for line in infile:
            parts = line.strip().split('\t')
            sample_name = parts[0]
            haplotype, positions = parts[1].split(':')
            start, end = positions.split('-')
            chromosome = parts[2]

            # Constructing the file path
            output_file = f"/home/alextu/scratch/centromere_analysis/CEN_COORD_UPDATED_Aug7_logsdon/haplotype_level_beds_complete_and_accurate_active_asat_HOR_arrays/{sample_name}_{haplotype}.bed"

            # Open the file handle if not already opened
            if output_file not in output_files:
                output_files[output_file] = open(output_file, 'w')

            # Formatting the output line as required
            output_line = f"{haplotype}\t{start}\t{end}\t{sample_name}\t{chromosome}\n"
            output_files[output_file].write(output_line)
finally:
    # Close all the file handles
    for f in output_files.values():
        f.close()
