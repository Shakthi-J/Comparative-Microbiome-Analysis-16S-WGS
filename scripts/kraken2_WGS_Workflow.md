Kraken2-Based Taxonomic Profiling of WGS Samples



This section describes the installation, database setup, execution, and downstream processing of Kraken2 for taxonomic classification of Whole Genome Shotgun (WGS) sequencing data.



1️⃣ Installation of Kraken2

Kraken2 can be installed either via Conda (recommended) or from source.

Install via Conda

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

conda install -c bioconda kraken2

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*



Add Kraken2 to your system PATH if required:

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

export PATH=$PATH:/path/to/kraken2

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*



Verify Installation

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

kraken2 --version

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*



2️⃣ Kraken2 Database Setup

Kraken2 requires a reference database for classification.

Available Options

Pre-built Kraken2 databases (standard, minikraken, etc.)

Custom-built databases (recommended for targeted studies)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

Example 

foldername/kraken2-standard-db/

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*



3️⃣ Preparation of WGS Samples

Input files are assembled contigs (.scaftig.fa)

Each sample is processed independently

Outputs include:

Classification output

Taxonomic summary report



4️⃣ Running Kraken2 on WGS Samples

Automated Batch Processing

The following loop runs Kraken2 on multiple samples and generates separate reports for each sample:

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

for sample in AH1 AW5 AK WM; do

&nbsp;   kraken2 \\

&nbsp;     --db foldername/kraken2-standard-db/ \\

&nbsp;     --use-names \\

&nbsp;     --report outputfoldername/${sample}\_report.txt \\

&nbsp;     --output outputfoldername/${sample}\_taxonomy\_kraken.txt \\

&nbsp;     folderpath\\ wgs/${sample}.scaftig.fa

done

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*



Individual Sample Execution (Optional, recommended if samples files are too large)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

kraken2 --db foldername/kraken2-standard-db/ --use-names \\

--report outputfoldername/AH1\_report.txt \\

--output outputfoldername/AH1\_taxonomy\_kraken.txt \\

folderpath\\ wgs/sample1.scaftig.fa

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*





5️⃣ Conversion of Kraken2 Reports to BIOM Format

Kraken2 reports are converted to a BIOM table for downstream analysis.

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

kraken-biom foldername/\*.txt -o foldername/taxonomic\_abundance.biom

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*



6️⃣ Conversion of BIOM to TSV Format

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

biom convert \\

&nbsp; -i foldername/taxonomic\_abundance.biom \\

&nbsp; -ofoldername/taxonomic\_abundance.tsv \\

&nbsp; --to-tsv

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*



7️⃣ Taxonomic Lineage Annotation Using TaxonKit

Taxonomic lineage information is added to sequence identifiers using TaxonKit (TaxonKit binary location: /home/miniconda3/bin/taxonkit).

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

cut -f2 sequences.tsv | \\

taxonkit lineage --data-dir /home/miniconda3/bin/taxonkit \\

> sequences\_with\_names.tsv

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*



📌 Output Files Generated



\*\_taxonomy\_kraken.txt → Kraken2 classification output



\*\_report.txt → Taxonomic summary report



taxonomic\_abundance.biom → BIOM-formatted abundance table



taxonomic\_abundance.tsv → Tab-separated abundance table



sequences\_with\_names.tsv → Lineage-annotated taxonomy file



