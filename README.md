# 16S rRNA vs Whole Genome Shotgun (WGS) Microbiome Analysis

## 🧬 Project Overview
Comparative microbiome analysis using 16S rRNA and whole genome shotgun (WGS) sequencing with reproducible QIIME 2 and Kraken2 pipelines.

- **16S rRNA amplicon sequencing**
- **Whole Genome Shotgun (WGS) sequencing**

The project focuses on understanding how the choice of sequencing strategy influences **taxonomic resolution, biological interpretation, and downstream analysis outcomes**.  
All workflows are implemented using **industry-standard bioinformatics tools** and automated through **Python-based pipelines** to ensure reproducibility and scalability.

This repository is intended as:
- A **research-ready microbiome analysis framework**
- A **demonstration of end-to-end bioinformatics workflow design**
- A **portfolio project showcasing practical NGS data analysis skills**

---

## 🎯 Project Goals
- Implement reproducible pipelines for **16S rRNA** and **WGS** microbiome data
- Compare taxonomic profiles derived from both sequencing approaches
- Highlight strengths and limitations of 16S vs WGS
- Provide clean, modular, and reusable analysis workflows

---

## 🧪 What This Project Covers

### 🔹 16S rRNA Analysis (QIIME 2)
- Manifest-based paired-end FASTQ import
- Quality assessment and demultiplexing
- Denoising and ASV generation using **DADA2**
- Feature table and representative sequence generation
- Taxonomic classification using reference databases
- Taxonomic visualization and phylogenetic tree construction
- Export of results for downstream statistical analysis

### 🔹 WGS Analysis (Kraken2)
- Taxonomic classification using **Kraken2**
- Batch processing of multiple samples
- Sample-wise taxonomic reports
- Abundance table generation (BIOM and TSV formats)
- Optional taxonomic lineage annotation

---

## 🛠️ Tools & Technologies Used
- **QIIME 2** – 16S rRNA amplicon analysis  
- **DADA2** – Error correction and denoising  
- **Kraken2** – WGS taxonomic classification  
- **kraken-biom / BIOM** – Abundance table generation  
- **TaxonKit** – Taxonomic lineage annotation  
- **Python** – Pipeline automation  
- **Shell scripting** – Workflow execution  
- **Conda** – Environment management  

---

📊 Key Takeaways

16S rRNA sequencing is cost-effective and suitable for community-level profiling

WGS sequencing provides higher taxonomic resolution and deeper biological insights

The choice of sequencing strategy significantly impacts microbiome interpretation

🔁 Reproducibility

Pipelines are fully automated using Python

Clear documentation is provided for each workflow

Conda environments ensure consistent software versions

⚠️ Note: Raw sequencing data is not included due to size and data-sharing constraints.
The repository focuses on workflows, scripts, and reproducibility.

⭐ If you find this repository useful, feel free to fork or star it.
