#!/usr/bin/env python3
"""
QIIME 2 16S rRNA Amplicon Analysis Pipeline
------------------------------------------

This script performs an end-to-end QIIME 2 workflow for 16S rRNA analysis:
1. Environment validation
2. Import of paired-end FASTQ files using a manifest
3. Demultiplexed data summary
4. Denoising using DADA2
5. Feature table and representative sequence visualization
6. Taxonomic classification
7. Taxonomic visualization
8. Export of taxonomy, feature table, and phylogenetic tree

Author: Shakthi
Project: 16S rRNA vs WGS Microbiome Analysis
"""

import subprocess
import os
from pathlib import Path

# -------------------- CONFIGURATION -------------------- #

# QIIME2 environment name (must be activated before running)
QIIME_ENV = "qiime2-amplicon-2024.5"

# Input files
MANIFEST_FILE = "....../manifest.tsv"
METADATA_FILE = "metadata.tsv"

# Output directory
OUTPUT_DIR = "qiime2_output"

# Classifier
CLASSIFIER = "my-new-classifier.qza"
SILVA_CLASSIFIER_URL = "https://data.qiime2.org/2023.9/common/silva-138-99-nb-classifier.qza"

# DADA2 parameters
TRIM_LEFT_F = 0
TRIM_LEFT_R = 0
TRUNC_LEN_F = 240
TRUNC_LEN_R = 240

# ------------------------------------------------------ #


def run_command(command: str):
    """Run shell commands safely."""
    print(f"\n[INFO] Running command:\n{command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {command}")


def check_qiime_installation():
    """Verify QIIME2 installation."""
    run_command("qiime --help")


def import_sequences():
    """Import paired-end FASTQ files using a manifest."""
    cmd = f"""
    qiime tools import \
      --type 'SampleData[PairedEndSequencesWithQuality]' \
      --input-path {MANIFEST_FILE} \
      --output-path {OUTPUT_DIR}/paired-end-demux.qza \
      --input-format PairedEndFastqManifestPhred33V2
    """
    run_command(cmd)


def summarize_demux():
    """Summarize demultiplexed sequences."""
    cmd = f"""
    qiime demux summarize \
      --i-data {OUTPUT_DIR}/paired-end-demux.qza \
      --o-visualization {OUTPUT_DIR}/demux.qzv
    """
    run_command(cmd)


def run_dada2():
    """Denoise sequences using DADA2."""
    cmd = f"""
    qiime dada2 denoise-paired \
      --i-demultiplexed-seqs {OUTPUT_DIR}/paired-end-demux.qza \
      --p-trim-left-f {TRIM_LEFT_F} \
      --p-trim-left-r {TRIM_LEFT_R} \
      --p-trunc-len-f {TRUNC_LEN_F} \
      --p-trunc-len-r {TRUNC_LEN_R} \
      --o-table {OUTPUT_DIR}/table.qza \
      --o-representative-sequences {OUTPUT_DIR}/rep-seqs.qza \
      --o-denoising-stats {OUTPUT_DIR}/denoising-stats.qza
    """
    run_command(cmd)


def summarize_denoising():
    """Summarize denoising statistics."""
    cmd = f"""
    qiime metadata tabulate \
      --m-input-file {OUTPUT_DIR}/denoising-stats.qza \
      --o-visualization {OUTPUT_DIR}/denoising-stats.qzv
    """
    run_command(cmd)


def summarize_feature_table():
    """Summarize feature table."""
    cmd = f"""
    qiime feature-table summarize \
      --i-table {OUTPUT_DIR}/table.qza \
      --o-visualization {OUTPUT_DIR}/table.qzv \
      --m-sample-metadata-file {METADATA_FILE}
    """
    run_command(cmd)


def visualize_rep_seqs():
    """Visualize representative sequences."""
    cmd = f"""
    qiime feature-table tabulate-seqs \
      --i-data {OUTPUT_DIR}/rep-seqs.qza \
      --o-visualization {OUTPUT_DIR}/rep-seqs.qzv
    """
    run_command(cmd)


def classify_taxonomy():
    """Perform taxonomic classification."""
    if not Path(CLASSIFIER).exists():
        print("[INFO] Classifier not found. Downloading SILVA classifier...")
        run_command(f"wget {SILVA_CLASSIFIER_URL}")
    
    cmd = f"""
    qiime feature-classifier classify-sklearn \
      --i-classifier {CLASSIFIER} \
      --i-reads {OUTPUT_DIR}/rep-seqs.qza \
      --o-classification {OUTPUT_DIR}/taxonomy.qza
    """
    run_command(cmd)


def visualize_taxonomy():
    """Generate taxonomy bar plots."""
    cmd = f"""
    qiime taxa barplot \
      --i-table {OUTPUT_DIR}/table.qza \
      --i-taxonomy {OUTPUT_DIR}/taxonomy.qza \
      --m-metadata-file {METADATA_FILE} \
      --o-visualization {OUTPUT_DIR}/taxa-bar-plots.qzv
    """
    run_command(cmd)


def export_results():
    """Export taxonomy and feature table."""
    run_command(f"qiime tools export --input-path {OUTPUT_DIR}/taxonomy.qza --output-path {OUTPUT_DIR}/exported-taxonomy")
    run_command(f"qiime tools export --input-path {OUTPUT_DIR}/table.qza --output-path {OUTPUT_DIR}/exported-feature-table")

    run_command(
        f"biom convert "
        f"--input-fp {OUTPUT_DIR}/exported-feature-table/feature-table.biom "
        f"--output-fp {OUTPUT_DIR}/feature-table.tsv "
        f"--to-tsv"
    )


def build_phylogeny():
    """Generate phylogenetic tree."""
    cmd = f"""
    qiime phylogeny align-to-tree-mafft-fasttree \
      --i-sequences {OUTPUT_DIR}/rep-seqs.qza \
      --o-alignment {OUTPUT_DIR}/aligned-rep-seqs.qza \
      --o-masked-alignment {OUTPUT_DIR}/masked-aligned-rep-seqs.qza \
      --o-tree {OUTPUT_DIR}/unrooted-tree.qza \
      --o-rooted-tree {OUTPUT_DIR}/rooted-tree.qza
    """
    run_command(cmd)

    run_command(
        f"qiime tools export "
        f"--input-path {OUTPUT_DIR}/rooted-tree.qza "
        f"--output-path {OUTPUT_DIR}/exported-tree"
    )


def main():
    print("\n=== QIIME 2 16S rRNA Pipeline Started ===")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    check_qiime_installation()
    import_sequences()
    summarize_demux()
    run_dada2()
    summarize_denoising()
    summarize_feature_table()
    visualize_rep_seqs()
    classify_taxonomy()
    visualize_taxonomy()
    export_results()
    build_phylogeny()

    print("\n=== QIIME 2 Pipeline Completed Successfully ===")


if __name__ == "__main__":
    main()
