# KCHlab demux-dada2

NEED TO UPDATE THIS WITH A DIFFERENT WEBSITE: VVV 
[![Documentation](https://img.shields.io/badge/docs-online-5b9aa0)](https://kchuang-lab.github.io/CUPID-seq/)


The following document describes how to use the Docker and Singularity/Apptainer images to use our demultiplexing code and run DADA2 on sequencing data. By using these containerization platforms, users can avoid the time consuming process of installing dependencies and configuring environments and conduct analyses in a highly reproducible manner. 

<img align="center" src="https://github.com/KCHuang-Lab/CUPID-seq/blob/main/docs/images/CUPID-seq-logo.png?raw=true" alt="Alt Text" width="150" height="500" >


**Contents:**
* [Overview](https://github.com/KCHuang-Lab/demux-dada2/blob/main/README.md#overview)
* [Run locally using Docker](https://github.com/KCHuang-Lab/demux-dada2/blob/main/README.md#run-locally-using-docker)
* [Run on Sherlock using Singularity/Apptainer](https://github.com/KCHuang-Lab/demux-dada2/blob/main/README.md#run-on-sherlock-using-singularity/apptainer)
* [Inputs](https://github.com/KCHuang-Lab/demux-dada2/blob/main/README.md#inputs)
* [Custom Primers](https://github.com/KCHuang-Lab/demux-dada2/blob/main/README.md#custom-primers)


## Overview
Once seqeuncing data is back from Biohub, the first round of demultiplexing (based on R2 primer plates) has already been conducted. The next step is to demultiplex based on R1 primers (the 8 phases) and analyze the data using DADA2. This can be done on your local system using Docker (LINK) or on Sherlock using Singularity/Apptainer (link). The instructions for each are below. 

## Run locally using Docker
### Setup:
1. **Install Docker:** To install Docker on your local system, follow the instructions [here](https://docs.docker.com/desktop/?_gl=1*f3oj9s*_gcl_au*ODUyODMyMDk5LjE3ODE3OTk4NzE.*_ga*MTQ4MDE1MzQwMC4xNzgxNzk5ODcx*_ga_XJWPQMJYHQ*czE3ODIzOTQ3NDkkbzIkZzEkdDE3ODIzOTQ3NTAkajU5JGwwJGgw).
2. **Prepare Inputs:** Next, prepare your input files, as described [here](https://kchuang-lab.github.io/CUPID-seq/configuration/). For the fastqlist, you will neet to provide a path for where the files will be located within the docker container. I recommend using a path like "./fastq_data/{run_name}/{read_name}" which is given relative to the  `16s-demux` directory. It will be easy to move in files and organize them within the existing `fastq_data` directory once the container is set up.

### Prep and run test analysis:
1. **Pull Image:** From the terminal, pull the Docker image by running: `docker pull rlporter24/demux-dada2:1.0`
2. **Launch Container:** Next, launch a container by running: `docker run -it rlporter24/demux-dada2:1.0`. Your terminal window will now exist within a Docker container based on the demux-dada2:1.0 image, which contains all the necessary packages and code for demultiplexing and running DADA2 on sequencing data.
3. **Transfer in Data:** From a separate terminal window, move in your raw sequencing data. If your data is stored on Oak or Sherlock currently, you will first need to move it to your local system (using SCP). Once data is local, copy it into the Docker container. You can find the container name by running `docker container ls`. Docker containers have the naming format {adjective}_{scientist surname}. To copy files into the docker container, run `docker cp {local_path} {CONTAINER}:{container_path}`. For example, you could run `docker cp  ./folder_with_reads practical_driscoll:/16s-demux/fastq_data/run_name/` to move the all the reads in `folder_with_reads` to a new folder within `fastq_data` named `run_name`.
4. **Transfer in Inputs:** Use the same procedure above to transfer your the fastq file list and sample sheet into the `/16s-demux/config/` directory. 
5. **Run Test Analysis:** Within the container terminal, navigate to the `16s-demux` directory and run: `snakemake -n`. This will run a 'dry run', where no code is executed, but the pipeline will output all steps to be run and ensure the necessary inputs exist. If the dry run is successful, run a real test analysis by running `snakemake --cores 4` (replacing the `4` with however many cores you want to use).
### Run real analysis:
6. **Edit config.yaml File:** To switch between the test and real analysis, navigate to the `/16s-demux/config/` directory and edit the `config.yaml` file. Line 2 should read `samplesheet: "config/15mc_003_samplesheet.txt" #samplesheet-Hremoved.txt"` and line 4 should read `fastqlist: "config/15mc_003_fastqlist.txt"`. Replace the files names in these lines with the names of you fastqlist and samplesheet, which should be located in the `16s-demux/config/` directory already (step 4). The text editor vim is available in the Docker container. 
7. **Edit Snakefile:** Next return to the `/16s-demux/` directory and edit line 4 from `configfile: "config/test_config.yaml"` to `configfile: "config/config.yaml"` to switch from running the test analysis to running the real analysis.
8. **Dryrun:** As before, run `snakemake -n` to do a dryrun to check the code and file structure without executing anything.
9. **Kick of the Analysis:** Run `snakemake --cores 4` (replacing `4` with your desired number of cores) to kick of a real run.
### Clean Up
10. **Transfer Outputs:** After the run, output files from the demultiplexing, filtering and trimming, and inference will be located within `/16s-demux/workflow/out/`. From an external terminal, run `docker cp {CONTAINER}:{container_path} {local path}` to transfer all files out. If you skip this step, the files will be deleted when you terminate the container.
11. **Close the Container:** Run `docker rm {CONTAINER}` to terminate the container. 




## Run on Sherlock using Singularity/Apptainer
### Setup:
1. **Install Snakemake**: Either install Snakemake locally (this is easy with Conda, instructions are [here](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html)) or use someone else's installation.
2. **Make a Temporary Copy of Code:** Copy the `/demux-dada2-files/` directory into $SCRATCH by running `cp -r /home/groups/kchuang/16s-demux-dada2/demux-dada2-files {temp $SCRATCH location}`.  The Singularity image is already built and located in $GROUP_HOME at `/home/groups/kchuang/16s-demux-dada2/demux-dada2-image.sif`, and you won't need to edit it or create a local copy.
3. **Transfer in Inputs:** Move your fastqlist and sample sheet into the `config` directory, at `.../demux-dada2-files/16s-demux/config/`.
4. **Update config.yaml:**  Replace the files names in lines 2 and 4 with the names of your fastqlist and samplesheet, which should be located in the `16s-demux/config/` directory already (step 4). The text editor vim is available in the Docker container. 
### Test run:
5. **Request Resources:** Run `sh_dev` to request additional resources. This will automatically give you one core and 4 GB memory for 1 hour, which is sufficient for the test analysis, but may not be enough for your full analysis. If you would like more cores, run `sh_dev -c N` for N cores or `sh_dev -t 02:00:00` for 2 hours rather than one. Additonal details on using a dev node are provided [here](https://www.sherlock.stanford.edu/docs/user-guide/running-jobs/#interactive-jobs).
6. **Activate Snakemake:** Next activate Snakemake either by running `conda activate snakemake` or `conda activate {path to someone else's snakemake}`. Once activated, you should see `(snakemake)` prefacing the command prompt.
7. **Test Dryrun:** Run a snakemake dry run for the test files to ensure that the environment is properly set up by running `snakemake -n -s test_Snakefile`.
8. **Test Run:** After the dry run, run a real test run with the command `snakemake -s test_Snakefile --cores 1 --use-singularity`. Be sure not to use more cores that you have requested for your sh_dev session. The run should take less than 10 minutes with one core. 
### Run real analysis
9. **Real Run:** Once the test run has completed successfully, run a real run using `Snakefile` instead of `test_Snakefile`. To do this, use the command `snakemake --cores 1 --use-singularity`. The time for this run will depend on the resources available and the number of samples you have. If a submission runs out of time, you can resume from where it left off by first unlocking the snakemake pipeline: `snakemake --unlock` and then resuming: `snakemake --cores 1 --use-singularity --rerun-incomplete`.
  
## Inputs
In addition to the sequencing data itself, there are two input files needed for demultiplexing: a fastq file list, and a sample sheet. Additionally, the included config.yaml file will need to be edited.\

**Note:** Most common issues in demultiplexing arise from errors in the input files. To help with troubleshooting, a quick check of the inputs will be conducted as the first step of the pipeline, and a summary will be output to '16s-demux/workflow/out/inputCheck_log.txt' (or '16s-demux/workflow/test_out/inputCheck_log.txt' for tests). If you encounter errors during the actual run but not in the test run, it may be helpful to check this log to ensure the inputs are properly formatted.  

1. **Fastq data:**\
  **Names:** Sample names should not include any spaces, underscores, or periods (hyphens are fine). If they do, they should be renamed before demultiplexing.\
   \
  **Format:** Files should be formatted as gzipped fastq files, or “.fastq.gz” files.\
   \
  **Location:** If the demultiplexing will be run locally or on a server, fastq files just need to be somewhere on that server. The paths to fastq files are defined by the entries included in 
the fastq file list and the config.yaml variable ‘fastqdir’. If the absolute path to the fastq files is provided in the fastq file list, then the fastqdir variable in config.yaml should be an empty string (“”). Otherwise, ensure that the ‘fastqdir’ path from config.yaml concatenated with the path in the fastq file list is correct.\
\
  For example, the file “/home/users/TEST/sequencing/exp01/fastqs/TEST_R1_001.fastq.gz” could be accurately described with the following combinations (and plenty others!):

| fastqdir:	(set in config.yaml) |	fastq file list: | 
| --- | --- |
| “”	|	“/home/users/TEST/sequencing/exp01/fastqs/TEST_R1_001.fastq.gz” |
| “/home/users/TEST/sequencing/exp01/fastqs/”	| “TEST_R1_001.fastq.gz” |

__Note:__ Periods in the samplenames are okay for this demultiplexing process, but are not for downstream analysis with some tools including DADA2. 

2. **Fastq file list:**\
  **Location:** The fastq file list should be located within the ‘config’ directory, and the file name should be updated in the fastqlist field of the ‘config.yaml’ file, (unless it is named ‘fastq.txt’, which is the default).\
   \
   **Contents:** The fastq list should be a tab-delimited text file, with the first column including the path to read 1, the second column including the path to read 2, and the final column including the shortened file name. This table should have headers of ‘read1’, ‘read2’, and ‘file’. For the file name, we recommend a format such as “{RunName}-{round2plate}-{well}”, where ‘RunName’ can be anything without underscores, spaces, or periods, and the next two terms specify the plate identifier for the round 2 barcodes and the well number respectively. It is essential that the ‘file’ field in the fastq file list matches the first part of the ‘filename’ field in the Samplesheet.\
   \
  The fastq file list for the test files is shown below:

| read1	|	read2	|	file |
| ------| ---- | ---- |
| ../fastq_data/test_inputs/KKRP-001_S441_R1_001.fastq.gz	| ../fastq_data/test_inputs/KKRP-001_S441_R2_001.fastq.gz | 15mc-003-P08B01-A01 |
| ../fastq_data/test_inputs/KKRP-002_S442_R1_001.fastq.gz	| ../fastq_data/test_inputs/KKRP-002_S442_R2_001.fastq.gz	| 15mc-003-P08B01-A02 |
| ../fastq_data/test_inputs/KKRP-003_S443_R1_001.fastq.gz	| ../fastq_data/test_inputs/KKRP-003_S443_R2_001.fastq.gz	| 15mc-003-P08B01-A03 |
| ../fastq_data/test_inputs/KKRP-004_S444_R1_001.fastq.gz	| ../fastq_data/test_inputs/KKRP-004_S444_R2_001.fastq.gz	| 15mc-003-P08B01-A04 |


3. **Samplesheet:**\
   **Location:** The samplesheet should be included in the ‘config’ directory, the ‘samplesheet’ path in the ‘config.yaml’ file should be updated to reflect the samplesheet’s name, unless it has the default name ‘samplesheet.txt’.\
   \
  **Contents:** The sample sheet will contain metadata for all the samples as a tab-delimited table (.tsv or .txt). This file should contain a header as the first row, and must include the following columns: ‘filename’, ‘sample’, and ‘group’. Additional columns can be included in the table. For example, the test samplesheet has columns 'No',	'RunName',	'plate',	'platename',	'well',	'R1index/phase',	'R2 plate',	'our file name',	'filename',	'sample',	and 'group'. Any extra column names can be included as desired, but ‘filename’, sample’ and ‘group’ are necessary.\
  The ‘sample’ column should contain the name that each individual sample will take after demultiplexing, and should not contain underscores or periods.\
  The ‘group’ column can contain any group identifier (without spaces or slashes). Samples in different groups will be output into different subdirectories within the ‘trimmed’ directory at the end of the run. If you don’t need reads separated, use one group specifier for all samples, or just leave the column blank (but do keep the ‘group’ header).\
  The ‘filename’ column should have the format:\
  `{RunName}-{round2plate}-{well}-L{round1index}`\
  with the ‘{RunName}-{round2plate}-{well}’ portion matching the corresponding ‘file’ entries in the fastq file list.\
  The 'round1index' should match the 'phase' entry in the indexfordemux.sh table.\
\
 Some of the columns from the test sample sheet are shown below:

| No	| RunName	| plate	| platename	| well	| R1index/phase	| R2 plate | our file name	| filename	| sample	| group |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 385	| 15mc-003	| P5	| plate5	| A01	| 4	| P08B01	| plateP-wellA1	| 15mc-003-P08B01-A01-L4	| P5-A01-plateP-wellA1	| group1 |
| 386	| 15mc-003	| P5	| plate5	| A02	| 4	| P08B01	| plateP-wellA2	| 15mc-003-P08B01-A02-L4	| P5-A02-plateP-wellA2	| group1 |
| 481	| 15mc-003	| P6	| plate6	| A01	| 5	| P08B01	| plateW-wellA5	| 15mc-003-P08B01-A01-L5	| P6-A01-plateW-wellA5	| group2 |
| 482	| 15mc-003	| P6	| plate6	| A02	| 5	| P08B01	| plateW-wellA6	| 15mc-003-P08B01-A02-L5	| P6-A02-plateW-wellA6	| group2 |



## Custom Primers
The instructions and code above all assume the primers and indexes used are the standard 16S V4 sets presented in the paper. If custom primers/indexes are used, several changes will need to be made.

1. **Update config/indexfordemux.txt**\
Make sure the indexfordemux.txt file (which contains the indicies used for demultiplexing R1 indicies) included in the config directory and specified in the 'config.yaml' file corresponds to the appropriate region. We provide primer sequences and corresponding 'indexfordemux.txt' files for the following 16S regions: V1 - V2, V1 - V3, V2 - V3, V3, V3 - V4, V4 - V5, V5, V5 - V7, V6, V6 - V7, V6 - V8, and V7 - V9. These are provided in the 'other indexfordemux' folder here, along with an Excel worksheet showing how these were derived, with a template for making additional primers ('other indexfordemux.xlsx').\
\
If you want to amplify another region, you can use this template to make a custom 'indexfordemux.sh' file. (To make a custom 'indexfordemux.sh' file in the 'other indexfordemux.xlsx' file, replace the entries in 'geneF' with the first part of the gene sequence (5' - 3', coding strand) and the entries in 'geneR' with the end of the gene sequence (5' - 3', template strand)).\
**(include image schematic of the reads with the index/spacer/genespecific region, etc?)**\
\
As a reminder, the final structure of reads after the library prep will look something like this (lengths not to scale):\
  <img src="https://github.com/KCHuang-Lab/CUPID-seq/blob/main/docs/images/primerStructureImage.png?raw=true" alt="Alt Text" width="400" height="400">\
The round 1 indexes have variable lengths or ‘phases’ as shown in the table and image below:

| phase | variable FP | variable RP |
| --- | --- | --- |
| 0 |  |ATGGACT |
| 1 | T | GCTAGC |
| 2 | GG  | TGACT |
| 3 | ACT | CGGT |
| 4 | TAAC | GTA |
| 5 | CAGTC | AA |
| 6 | ATCGAT | C|
| 7 | GCAAGTC  | |

 <img src="https://github.com/KCHuang-Lab/CUPID-seq/blob/main/docs/images/phasedPrimerImage.png?raw=true" alt="Alt Text" width="400" height="400">

However, during the demultiplexing, we treat the reads as if they have 7 base pair indexes on both ends. Any of the 7 base pairs that are not filled in with the index will be the spacer/gene-specific primer sequence. The table below shows the default indexes, with the actual index base pairs underlined, the spacer base pairs in lowercase, and the gene-specific primer regions uppercase and bolded. (The ‘bc’ or barcode column is simply the concatenated strings of read1index and read2index). The index, spacer, and gene specific regions will need to be edited according to the changes made.\

| phase | read1index | read2index | bc |
| --- | --- | --- | --- |
| 0 | cagt**AGA** | <ins>ATGGACT</ins> | CAGTAGAATGGACT | 
| 1 | <ins>T</ins>cagt**AG** | <ins>GCTAGC</ins>a | TCAGTAGGCTAGCA | 
| 2 | <ins>GG</ins>cagt**A** | <ins>TGACT</ins>at | GGCAGTATGACTAT | 
| 3 | <ins>ACT</ins>cagt | <ins>CGGT</ins>atc | ACTCAGTCGGTATC | 
| 4 | <ins>TAAC</ins>cag | <ins>GTA</ins>atcc | TAACCAGGTAATCC | 
| 5 | <ins>CAGTC</ins>ca | <ins>AA</ins>atcc**T** | CAGTCCAAAATCCT | 
| 6 | <ins>ATCGAT</ins>c | <ins>C</ins>atcc**TA** | ATCGATCCATCCTA | 
| 7 | <ins>GCAAGTC</ins> | atcc**TAC** | GCAAGTCATCCTAC |

If the same primer design and index scheme is used, and only the gene-specific region is changed, only the gene-specific regions within the indices will need to be updated. For the primers above, the gene of interest starts with 'AGA...' and ends with 'GTA' on the forward strand, hence the regions of homology include 'AGA' and 'TAC', both in the 5' to 3' direction.\
\
For a gene reading 'ATG ... CGT', the regions of homology within primers would become 'ATG' and 'ACG', both in the 5' to 3' direction. Thus the indexfordemux table should be edited to:

| phase | read1index | read2index | bc |
| --- | --- | --- | --- |
| 0 | cagt**ATG** | <ins>ATGGACT</ins> | CAGTAGAATGGACT | 
| 1 | <ins>T</ins>cagt**AT** | <ins>GCTAGC</ins>a | TCAGTAGGCTAGCA | 
| 2 | <ins>GG</ins>cagt**A** | <ins>TGACT</ins>at | GGCAGTATGACTAT | 
| 3 | <ins>ACT</ins>cagt | <ins>CGGT</ins>atc | ACTCAGTCGGTATC | 
| 4 | <ins>TAAC</ins>cag | <ins>GTA</ins>atcc | TAACCAGGTAATCC | 
| 5 | <ins>CAGTC</ins>ca | <ins>AA</ins>atcc**A** | CAGTCCAAAATCCT | 
| 6 | <ins>ATCGAT</ins>c | <ins>C</ins>atcc**AC** | ATCGATCCATCCTA | 
| 7 | <ins>GCAAGTC</ins> | atcc**ACG** | GCAAGTCATCCTAC |

Note that only the gene-specific regions have changed, and the index and spacer sequences are identical to the initial set.

__Note:__ We recommend avoiding any mixed base characters such as ‘W’ or ‘N’ in the first three positions of your gene specific primer. If such bases are included, you will need to include extra entries in the indexfordemux.txt table, one for each potential base (e.g., for a ‘W’, one version should have an ‘A’ and one should have a ‘T’). Each sample with a mixed base index should thus be included twice in the samplesheet, and the output files will then need to be merged downstream (either after trimming or after subsequent analyses).

2. **Update the index lengths in config/config.yaml**\ 
Within the ‘config/config.yaml’ file, the index/primer lengths may need to be updated. The “lenR1index” and “lenR2index” should be set to the longest version of these (e.g., in the provided primer/index set, the longest sequence of index bases is 7, so the value is set to 7). The “lenR1primer” and “lenR2primer” values should be set to equal the length of the gene-specific primer sequence plus the length of the spacer. For the 16S sets with provided indexfordemux.txt files (V1 - V2, V1 - V3, V2 - V3, V3, V3 - V4, V4 - V5, V5, V5 - V7, V6, V6 - V7, V6 - V8, and V7 - V9), the lengths do not need to be changed; the defaults below are correct.

| Region | length | 
| --- | --- | 
| lenR1primer |  23 | 
| lenR2primer | 24 | 
| lenR1index | 7 | 
| lenR2index | 7 |
