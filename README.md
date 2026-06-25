# KCHlab demux-dada2

NEED TO UPDATE THIS WITH A DIFFERENT WEBSITE: VVV 
[![Documentation](https://img.shields.io/badge/docs-online-5b9aa0)](https://kchuang-lab.github.io/CUPID-seq/)


The following document describes how to use the Docker and Singularity/Apptainer images to use our demultiplexing code and run DADA2 on sequencing data. By using these containerization platforms, users can avoid the time consuming process of installing dependencies and configuring environments and conduct analyses in a highly reproducible manner. 

<img align="center" src="https://github.com/KCHuang-Lab/CUPID-seq/blob/main/docs/images/CUPID-seq-logo.png?raw=true" alt="Alt Text" width="150" height="500" >



NONE OF THE LINKS BELOW ARE VALID!!! UPDATE!!!

**Contents:**
* [Overview] (https://github.com/KCHuang-Lab/CUPID-seq/blob/main/README.md#using-docker)
* [Run locally using Docker](https://github.com/KCHuang-Lab/CUPID-seq/blob/main/README.md#using-docker)
* [Run on Sherlock using Singularity/Apptainer](https://github.com/KCHuang-Lab/CUPID-seq/blob/main/README.md#using-singularityapptainer)
* [Inputs](https://github.com/KCHuang-Lab/CUPID-seq/blob/main/README.md#inputs)
* [Custom Primers](https://github.com/KCHuang-Lab/CUPID-seq/blob/main/README.md#custom-primers)


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

