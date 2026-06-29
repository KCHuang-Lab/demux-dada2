#!/bin/bash
#SBATCH --job-name=submitSnakemake
#SBATCH --time=1:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G

# Additional specifications:
# SBATCH --mail-user=youremail@email.com
# SBATCH -p nodeName

singularity build demux-dada2-image.sif dada2.def
