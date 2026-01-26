## Kraken2-Based Taxonomic Profiling of WGS Samples

This section describes the installation, database setup, execution, and downstream processing of **Kraken2** for taxonomic classification of Whole Genome Shotgun (WGS) sequencing data.

---

## 1️⃣ Installation of Kraken2

Kraken2 can be installed either via **Conda** (recommended) or from source.

Install via Conda
conda install -c bioconda kraken2
```

Add Kraken2 to your system `PATH` if required:

```bash
export PATH=$PATH:/path/to/kraken2
```

### Verify Installation

```bash
kraken2 --version
```

---

## 2️⃣ Kraken2 Database Setup

Kraken2 requires a reference database for classification.

### Available Options

* **Pre-built Kraken2 databases** (standard, minikraken, etc.)
* **Custom-built databases** (recommended for targeted studies)

> ⚠️ Database build and download commands are provided in the repository under the database setup section.

Example database path used in this analysis:

```text
Naveed/kraken2-standard-db/
```

---

## 3️⃣ Preparation of WGS Samples

* Input files are assembled contigs (`.scaftig.fa`)
* Each sample is processed independently
* Outputs include:

  * Classification output
  * Taxonomic summary report

---

## 4️⃣ Running Kraken2 on WGS Samples

### Automated Batch Processing

The following loop runs Kraken2 on multiple samples and generates **separate reports for each sample**:

```bash
for samples; do
    kraken2 \
      --db folderpath/kraken2-standard-db/ \
      --use-names \
      --report outputfolderpath/${sample}_report.txt \
      --output outputfolderpath/${sample}_taxonomy_kraken.txt \
      / wgs/${sample}.scaftig.fa
done
```

---

### Individual Sample Execution (Optional)

```bash
kraken2 --db Naveed/kraken2-standard-db/ --use-names \
--report outputfolderpath/sample1_report.txt \
--output outputfolderpath/sample1_taxonomy_kraken.txt \
\ wgs/AH1.scaftig.fa
```
---

## 5️⃣ Conversion of Kraken2 Reports to BIOM Format

Kraken2 reports are converted to a **BIOM table** for downstream analysis.

### With Path Specification

```bash
kraken-biom outputfolderpath/*.txt -o outputfolderpath/taxonomic_abundance.biom
```

### Without Path Specification

```bash
kraken-biom *.txt -o taxonomic_abundance.biom
```

---

## 6️⃣ Conversion of BIOM to TSV Format

### With Path

```bash
biom convert \
  -i outputfolderpath/taxonomic_abundance.biom \
  -o outputfolderpath/taxonomic_abundance.tsv \
  --to-tsv
```

### Without Path

```bash
biom convert \
  -i taxonomic_abundance.biom \
  -o taxonomic_abundance.tsv \
  --to-tsv
```

---

## 7️⃣ Taxonomic Lineage Annotation Using TaxonKit

Taxonomic lineage information is added to sequence identifiers using **TaxonKit**.

```bash
cut -f2 sequences.tsv | \
taxonkit lineage --data-dir /home/miniconda3/bin/taxonkit \
> sequences_with_names.tsv
```

TaxonKit binary location:

```text
/home/miniconda3/bin/taxonkit
```

---

## 📌 Output Files Generated

* `*_taxonomy_kraken.txt` → Kraken2 classification output
* `*_report.txt` → Taxonomic summary report
* `taxonomic_abundance.biom` → BIOM-formatted abundance table
* `taxonomic_abundance.tsv` → Tab-separated abundance table
* `sequences_with_names.tsv` → Lineage-annotated taxonomy file

---
