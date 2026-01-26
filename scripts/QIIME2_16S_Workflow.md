# QIIME 2–Based 16S rRNA Amplicon Sequencing Analysis Pipeline

## 📌 Overview
This document describes a reproducible **QIIME 2 workflow** for analyzing **16S rRNA amplicon sequencing data**.  
The pipeline includes environment setup, data import using a manifest file, denoising with DADA2, taxonomic classification, visualization, and export of results for downstream analysis.

This workflow is part of a **comparative study between 16S rRNA and Whole Genome Shotgun (WGS) sequencing approaches**.

---

## 🛠️ Prerequisites
- Linux-based system
- Conda / Miniconda installed
- Internet access for downloading reference classifiers
- Input FASTQ files (paired-end)
- Manifest file (`manifest.tsv`)
- Metadata file (`metadata.tsv`)

---

## 1️⃣ QIIME 2 Installation

Create and install the QIIME 2 amplicon environment:

```bash
conda env create -n qiime2 \
  --file https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2024.10-py310-linux-conda.yml
````

Activate the environment:

```bash
conda activate qiime2
```

Verify the installation:

```bash
qiime --help
```

---

## 2️⃣ Pre-processing Requirements

Before running the QIIME 2 workflow, ensure the following files are prepared:

### Manifest File

* Created using a custom script (e.g., `manifest.sh`)
* Specifies absolute paths to paired-end FASTQ files
* Format: `PairedEndFastqManifestPhred33V2`

### Metadata File

* Retrieved or constructed using NCBI/SRA sample information
* Must contain a column named **`sample-id`**
* Saved as `metadata.tsv`

---

## 3️⃣ Activate QIIME 2 Environment

```bash
conda activate qiime2-amplicon-2024.5
```

---

## 4️⃣ Importing Paired-End Sequences

```bash
qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path .../manifest.tsv \
  --output-path paired-end-demux.qza \
  --input-format PairedEndFastqManifestPhred33V2
```

---

## 5️⃣ Summarizing Demultiplexed Data

```bash
qiime demux summarize \
  --i-data paired-end-demux.qza \
  --o-visualization demux.qzv
```

View the visualization:

```bash
qiime tools view demux.qzv
```

---

## 6️⃣ Denoising with DADA2

```bash
qiime dada2 denoise-paired \
  --i-demultiplexed-seqs paired-end-demux.qza \
  --p-trim-left-f 0 \
  --p-trim-left-r 0 \
  --p-trunc-len-f 240 \
  --p-trunc-len-r 240 \
  --o-table table.qza \
  --o-representative-sequences rep-seqs.qza \
  --o-denoising-stats denoising-stats.qza
```

---

## 7️⃣ Summarizing Denoising Statistics

```bash
qiime metadata tabulate \
  --m-input-file denoising-stats.qza \
  --o-visualization denoising-stats.qzv
```

View the statistics:

```bash
qiime tools view denoising-stats.qzv
```

---

## 8️⃣ Summarizing the Feature Table

```bash
qiime feature-table summarize \
  --i-table table.qza \
  --o-visualization table.qzv \
  --m-sample-metadata-file metadata.tsv
```

View the summary:

```bash
qiime tools view table.qzv
```

---

## 9️⃣ Visualizing Representative Sequences

```bash
qiime feature-table tabulate-seqs \
  --i-data rep-seqs.qza \
  --o-visualization rep-seqs.qzv
```

View the sequences:

```bash
qiime tools view rep-seqs.qzv
```

---

## 🔬  Taxonomic Classification

### Reference Classifier

Download the SILVA reference classifier:

```bash
wget https://data.qiime2.org/2023.9/common/silva-138-99-nb-classifier.qza
```

Alternatively, a custom classifier (e.g., `gg-13-8-99-515-806-nb-classifier.qza`) can be used.

### Classification Command

```bash
qiime feature-classifier classify-sklearn \
  --i-classifier my-new-classifier.qza \
  --i-reads rep-seqs.qza \
  --o-classification taxonomy.qza
```

---

##  Visualizing Taxonomic Composition

```bash
qiime taxa barplot \
  --i-table table.qza \
  --i-taxonomy taxonomy.qza \
  --m-metadata-file metadata.tsv \
  --o-visualization taxa-bar-plots.qzv
```

View the visualization:

```bash
qiime tools view taxa-bar-plots.qzv
```

---

##  Exporting Taxonomy Data

```bash
qiime tools export \
  --input-path taxonomy.qza \
  --output-path exported-taxonomy
```

View exported taxonomy:

```bash
cat exported-taxonomy/taxonomy.tsv
```

---

##  Exporting the Feature Table

```bash
qiime tools export \
  --input-path table.qza \
  --output-path exported-feature-table
```

Convert BIOM to TSV:

```bash
biom convert \
  --input-fp exported-feature-table/feature-table.biom \
  --output-fp feature-table.tsv \
  --to-tsv
```

---

## 🌳  Phylogenetic Tree Construction

```bash
qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences rep-seqs.qza \
  --o-alignment aligned-rep-seqs.qza \
  --o-masked-alignment masked-aligned-rep-seqs.qza \
  --o-tree unrooted-tree.qza \
  --o-rooted-tree rooted-tree.qza
```

---

##  Exporting the Phylogenetic Tree

```bash
qiime tools export \
  --input-path rooted-tree.qza \
  --output-path exported-tree
```

---

## 📂 Output Files Generated

* `table.qza` – Feature table
* `rep-seqs.qza` – Representative sequences
* `taxonomy.qza` – Taxonomic assignments
* `taxa-bar-plots.qzv` – Taxonomic visualization
* `feature-table.tsv` – Exported abundance table
* `rooted-tree.qza` – Phylogenetic tree

---

## ✅ Notes

* Ensure `metadata.tsv` contains a column named **`sample-id`**
* Trimming and truncation parameters should be adjusted based on quality plots
* This pipeline is designed for **paired-end 16S rRNA data**

