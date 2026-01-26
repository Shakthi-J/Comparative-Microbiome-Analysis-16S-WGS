#!/usr/bin/env python3
"""
Kraken2-based Taxonomic Profiling Pipeline for WGS Samples
----------------------------------------------------------

This script performs:
1. Kraken2 taxonomic classification for multiple WGS samples
2. Generation of individual Kraken2 reports
3. Conversion of Kraken2 reports to BIOM format
4. Conversion of BIOM to TSV format
5. Optional taxonomic lineage annotation using TaxonKit

Author: Shakthi
Project: 16S rRNA vs WGS Microbiome Analysis
"""

import subprocess
import os
from pathlib import Path

# -------------------- CONFIGURATION -------------------- #

# Paths
KRAKEN_DB = "foldername/kraken2-standard-db"
WGS_DATA_DIR = "folderpath"
OUTPUT_DIR = "outputfolderpath"

# Samples to process
SAMPLES = ["AB1", "CD2", "EF3", "GH4"]

# Tools
KRAKEN2_CMD = "kraken2"
KRAKEN_BIOM_CMD = "kraken-biom"
BIOM_CMD = "biom"
TAXONKIT_CMD = "taxonkit"

# TaxonKit data directory (update if needed)
TAXONKIT_DATA_DIR = "/home/miniconda3/bin/taxonkit"

# ------------------------------------------------------- #


def run_command(command: str):
    """Run a shell command and handle errors."""
    print(f"\n[INFO] Running command:\n{command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {command}")


def run_kraken2():
    """Run Kraken2 for each WGS sample."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for sample in SAMPLES:
        input_fasta = f"{WGS_DATA_DIR}/{sample}.scaftig.fa"
        report_file = f"{OUTPUT_DIR}/{sample}_report.txt"
        output_file = f"{OUTPUT_DIR}/{sample}_taxonomy_kraken.txt"

        cmd = (
            f"{KRAKEN2_CMD} "
            f"--db {KRAKEN_DB} "
            f"--use-names "
            f"--report {report_file} "
            f"--output {output_file} "
            f"\"{input_fasta}\""
        )

        run_command(cmd)


def convert_to_biom():
    """Convert Kraken2 reports to BIOM format."""
    biom_output = f"{OUTPUT_DIR}/taxonomic_abundance.biom"
    cmd = f"{KRAKEN_BIOM_CMD} {OUTPUT_DIR}/*.txt -o {biom_output}"
    run_command(cmd)


def convert_biom_to_tsv():
    """Convert BIOM file to TSV format."""
    biom_file = f"{OUTPUT_DIR}/taxonomic_abundance.biom"
    tsv_output = f"{OUTPUT_DIR}/taxonomic_abundance.tsv"

    cmd = (
        f"{BIOM_CMD} convert "
        f"-i {biom_file} "
        f"-o {tsv_output} "
        f"--to-tsv"
    )

    run_command(cmd)


def annotate_taxonomy():
    """
    Annotate taxonomic lineages using TaxonKit.
    Requires a 'sequences.tsv' file in the working directory.
    """
    input_file = "sequences.tsv"
    output_file = "sequences_with_names.tsv"

    if not Path(input_file).exists():
        print("[WARNING] sequences.tsv not found. Skipping TaxonKit step.")
        return

    cmd = (
        f"cut -f2 {input_file} | "
        f"{TAXONKIT_CMD} lineage "
        f"--data-dir {TAXONKIT_DATA_DIR} "
        f"> {output_file}"
    )

    run_command(cmd)


def main():
    print("\n=== Kraken2 WGS Pipeline Started ===")

    run_kraken2()
    convert_to_biom()
    convert_biom_to_tsv()
    annotate_taxonomy()

    print("\n=== Pipeline Completed Successfully ===")


if __name__ == "__main__":
    main()
