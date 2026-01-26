#!/bin/bash
# Define the directory containing your fastq files
fastq_dir="./"  # Use current directory instead of absolute path

# Output file for the manifest
manifest_file="manifest.tsv"  # Use .tsv extension for tab-separated values

# Print the header (with tabs between column names)
echo -e "sample-id\tforward-absolute-filepath\treverse-absolute-filepath" > "$manifest_file"

# Loop through each sample's R1 (forward) fastq.gz file and generate entries
for f in "$fastq_dir"*R1_001.fastq.gz; do
  # Ensure we only process files that exist
  if [[ -e $f ]]; then
    # Extract the sample ID from the filename (taking everything before _L001)
    base_sample=$(basename "$f" | sed 's/_L001_R1_001\.fastq\.gz//')
    
    # Create sample ID based on the base_sample
    sample_id="${base_sample}"
    
    # Construct the reverse read filename by replacing R1 with R2
    reverse_file="${f/R1_001.fastq.gz/R2_001.fastq.gz}"
    
    # Get absolute paths for the files
    absolute_f=$(realpath "$f")
    absolute_reverse=$(realpath "$reverse_file")
    
    # Debugging statements
    echo "Processing forward file: $f"
    echo "Sample ID: $sample_id"
    
    # Write the entry to the manifest if the reverse file exists
    if [[ -e $reverse_file ]]; then
      echo -e "$sample_id\t$absolute_f\t$absolute_reverse" >> "$manifest_file"
      echo "Found reverse file: $reverse_file"
    else
      echo "Warning: Reverse file not found for sample $base_sample: $reverse_file"
    fi
  else
    echo "Warning: Forward file not found: $f"
  fi
done

echo "Manifest file created: $manifest_file"
